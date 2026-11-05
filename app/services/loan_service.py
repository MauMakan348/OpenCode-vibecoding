from app import validators
from app.database import get_db
from app.errors import BusinessRuleError, NotFoundError, ValidationError
from app.repositories import item_repository, loan_repository


def create_loan(data):
    """Validate input, take stock, and record a BORROWED loan atomically."""
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")

    student_id = validators.require_text(data.get("student_id"), "student_id")
    item_id = validators.require_positive_int(data.get("item_id"), "item_id")
    quantity = validators.require_positive_int(data.get("quantity"), "quantity")

    db = get_db()
    item = item_repository.get_item_by_id(db, item_id)
    if item is None:
        raise NotFoundError("Item not found")
    if quantity > item["available_stock"]:
        raise BusinessRuleError("Insufficient stock")

    try:
        if not item_repository.decrement_available_stock(db, item_id, quantity):
            raise BusinessRuleError("Insufficient stock")
        loan_id = loan_repository.create_loan(db, student_id, item_id, quantity)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return dict(loan_repository.get_loan_by_id(db, loan_id))


def return_loan(loan_id):
    """Mark a BORROWED loan RETURNED and restore stock atomically."""
    db = get_db()
    loan = loan_repository.get_loan_by_id(db, loan_id)
    if loan is None:
        raise NotFoundError("Loan not found")
    if loan["status"] == "RETURNED":
        raise BusinessRuleError("Loan already returned")

    try:
        if not loan_repository.mark_returned(db, loan_id):
            raise BusinessRuleError("Loan cannot be returned")
        item_repository.increment_available_stock(db, loan["item_id"], loan["quantity"])
        db.commit()
    except Exception:
        db.rollback()
        raise

    return dict(loan_repository.get_loan_by_id(db, loan_id))


def get_student_loans(student_id):
    """Return loans for one student, newest first."""
    return [
        dict(row)
        for row in loan_repository.get_loans_by_student_id(get_db(), student_id)
    ]
