from flask import Blueprint, jsonify, request

from app.services import item_service

bp = Blueprint("items", __name__, url_prefix="/items")


@bp.get("")
def get_items():
    """GET /items - list every item with current stock."""
    return jsonify({"data": item_service.list_items()})


@bp.post("")
def post_item():
    """POST /items - create an item."""
    return jsonify({"data": item_service.add_item(request.get_json(silent=True))}), 201
