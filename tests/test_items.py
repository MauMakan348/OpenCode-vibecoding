def test_get_items_when_database_empty(client):
    response = client.get("/items")

    assert response.status_code == 200
    assert response.get_json() == {"data": []}


def test_add_item_with_valid_data(client):
    response = client.post(
        "/items", json={"name": "Multimeter", "total_stock": 10}
    )

    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["name"] == "Multimeter"
    assert data["total_stock"] == 10
    assert data["available_stock"] == 10
    assert data["id"] == 1


def test_add_item_without_name(client):
    response = client.post("/items", json={"total_stock": 10})

    assert response.status_code == 400
    assert response.get_json() == {"error": "name is required"}


def test_add_item_with_negative_stock(client):
    response = client.post("/items", json={"name": "Multimeter", "total_stock": -1})

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_initial_available_stock_equals_total_stock(client):
    response = client.post(
        "/items", json={"name": "Multimeter", "total_stock": 7}
    )

    data = response.get_json()["data"]
    assert data["available_stock"] == data["total_stock"] == 7
