import pytest

from app import create_app
from app.database import init_db


@pytest.fixture
def app(tmp_path):
    """Fresh application with an isolated SQLite database per test."""
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test.db"),
        }
    )
    with app.app_context():
        init_db()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def item(client):
    """A Multimeter with total_stock 10."""
    response = client.post(
        "/items", json={"name": "Multimeter", "total_stock": 10}
    )
    return response.get_json()["data"]
