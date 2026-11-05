from app import validators
from app.database import get_db
from app.errors import ValidationError
from app.repositories import item_repository


def list_items():
    """Return every item with its current stock."""
    return [dict(row) for row in item_repository.get_all_items(get_db())]


def add_item(data):
    """Validate input, create an item, and return it as a dict."""
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")

    name = validators.require_text(data.get("name"), "name")
    total_stock = validators.require_non_negative_int(
        data.get("total_stock"), "total_stock"
    )

    db = get_db()
    try:
        item_id = item_repository.create_item(
            db, name, total_stock, available_stock=total_stock
        )
        db.commit()
    except Exception:
        db.rollback()
        raise

    return dict(item_repository.get_item_by_id(db, item_id))
