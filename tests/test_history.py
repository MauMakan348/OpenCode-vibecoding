def _create_loan(client, item, student_id, quantity=2):
    return client.post(
        "/loans",
        json={"student_id": student_id, "item_id": item["id"], "quantity": quantity},
    )


def test_history_with_loans_for_student(client, item):
    _create_loan(client, item, "20240001")
    _create_loan(client, item, "20240001", quantity=1)

    response = client.get("/loans/student/20240001")

    assert response.status_code == 200
    assert len(response.get_json()["data"]) == 2


def test_history_without_loans_returns_empty_list(client):
    response = client.get("/loans/student/20240001")

    assert response.status_code == 200
    assert response.get_json() == {"data": []}


def test_history_only_contains_requested_student(client, item):
    _create_loan(client, item, "20240001")
    _create_loan(client, item, "20240002", quantity=3)

    loans = client.get("/loans/student/20240001").get_json()["data"]

    assert len(loans) == 1
    assert all(loan["student_id"] == "20240001" for loan in loans)
