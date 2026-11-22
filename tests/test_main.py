from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_get_delete_item():
    created = client.post("/items", json={"name": "Pen", "price": 1.5})
    assert created.status_code == 201
    item_id = created.json()["id"]

    fetched = client.get(f"/items/{item_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Pen"

    assert client.delete(f"/items/{item_id}").status_code == 204
    assert client.get(f"/items/{item_id}").status_code == 404


def test_create_item_rejects_non_positive_price():
    resp = client.post("/items", json={"name": "Free", "price": 0})
    assert resp.status_code == 422


def test_list_items_paginated():
    for i in range(3):
        client.post("/items", json={"name": f"Item {i}", "price": 1})
    resp = client.get("/items?page=1&page_size=2")
    assert resp.status_code == 200
