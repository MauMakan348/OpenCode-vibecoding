from flask import Blueprint, jsonify, request

from app.services import loan_service

bp = Blueprint("loans", __name__, url_prefix="/loans")


@bp.post("")
def post_loan():
    """POST /loans - create a loan and take stock."""
    return jsonify({"data": loan_service.create_loan(request.get_json(silent=True))}), 201


@bp.put("/<int:loan_id>/return")
def put_return(loan_id):
    """PUT /loans/{id}/return - return the loan and restore stock."""
    return jsonify({"data": loan_service.return_loan(loan_id)})


@bp.get("/student/<student_id>")
def get_student_loans(student_id):
    """GET /loans/student/{student_id} - loan history for one NIM."""
    return jsonify({"data": loan_service.get_student_loans(student_id)})
