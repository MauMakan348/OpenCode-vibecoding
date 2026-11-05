def _create_loan(client, item, quantity=3):
    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": quantity},
    )
    return response.get_json()["data"]


def _available_stock(client):
    return client.get("/items").get_json()["data"][0]["available_stock"]


def test_return_loan_with_valid_data(client, item):
    loan = _create_loan(client, item)

    response = client.put(f"/loans/{loan['id']}/return")

    assert response.status_code == 200
    assert response.get_json()["data"]["id"] == loan["id"]


def test_return_loan_changes_status_to_returned(client, item):
    loan = _create_loan(client, item)

    response = client.put(f"/loans/{loan['id']}/return")

    assert response.get_json()["data"]["status"] == "RETURNED"


def test_return_loan_restores_stock_by_quantity(client, item):
    loan = _create_loan(client, item, quantity=4)
    assert _available_stock(client) == 6

    client.put(f"/loans/{loan['id']}/return")

    assert _available_stock(client) == 10


def test_return_unknown_loan(client):
    response = client.put("/loans/999/return")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Loan not found"}


def test_return_already_returned_loan(client, item):
    loan = _create_loan(client, item)
    client.put(f"/loans/{loan['id']}/return")

    response = client.put(f"/loans/{loan['id']}/return")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Loan already returned"}


def test_double_return_does_not_increase_stock(client, item):
    loan = _create_loan(client, item, quantity=4)
    client.put(f"/loans/{loan['id']}/return")
    client.put(f"/loans/{loan['id']}/return")

    assert _available_stock(client) == 10
