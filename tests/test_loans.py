import pytest


def test_create_loan_with_valid_data(client, item):
    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 2},
    )

    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["student_id"] == "20240001"
    assert data["item_id"] == item["id"]
    assert data["quantity"] == 2
    assert data["status"] == "BORROWED"


def test_create_loan_when_stock_is_sufficient(client, item):
    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 10},
    )

    assert response.status_code == 201
    items = client.get("/items").get_json()["data"]
    assert items[0]["available_stock"] == 0


def test_create_loan_when_quantity_exceeds_stock(client, item):
    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 11},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Insufficient stock"}


def test_create_loan_with_unknown_item(client):
    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": 999, "quantity": 1},
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Item not found"}


@pytest.mark.parametrize("quantity", [0, -1])
def test_create_loan_with_non_positive_quantity(client, item, quantity):
    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": quantity},
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_stock_decreases_by_quantity(client, item):
    client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 3},
    )

    items = client.get("/items").get_json()["data"]
    assert items[0]["available_stock"] == 7


def test_failed_loan_does_not_change_stock(client, item):
    client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 99},
    )

    items = client.get("/items").get_json()["data"]
    assert items[0]["available_stock"] == 10
    history = client.get("/loans/student/20240001").get_json()["data"]
    assert history == []


def test_loan_rolls_back_stock_when_record_creation_fails(
    client, item, monkeypatch
):
    from app.repositories import loan_repository

    def boom(*args, **kwargs):
        raise RuntimeError("simulated failure")

    monkeypatch.setattr(loan_repository, "create_loan", boom)

    with pytest.raises(RuntimeError):
        client.post(
            "/loans",
            json={"student_id": "20240001", "item_id": item["id"], "quantity": 4},
        )

    items = client.get("/items").get_json()["data"]
    assert items[0]["available_stock"] == 10
    assert client.get("/loans/student/20240001").get_json()["data"] == []
