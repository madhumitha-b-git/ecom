"""Unit tests for order endpoints."""

from unittest.mock import MagicMock
from bson import ObjectId

FAKE_ID = str(ObjectId())
ORDER_PAYLOAD = {
    "user_id": "user1",
    "product_id": "prod_001",
    "quantity": 2,
    "amount": 99.98,
}


def _inventory_doc(stock: int) -> dict:
    return {"_id": ObjectId(), "product_id": "prod_001", "stock": stock}


def test_create_order_success(client, mock_collections):
    mock_collections["inventory"].find_one.return_value = _inventory_doc(10)
    mock_collections["payments"].insert_one.return_value = MagicMock()
    mock_collections["inventory"].update_one.return_value = MagicMock()
    mock_collections["orders"].insert_one.return_value = MagicMock(inserted_id=ObjectId(FAKE_ID))

    res = client.post("/orders", json=ORDER_PAYLOAD)
    assert res.status_code == 201
    assert res.json()["order_id"] == FAKE_ID


def test_create_order_out_of_stock(client, mock_collections):
    mock_collections["inventory"].find_one.return_value = _inventory_doc(1)
    res = client.post("/orders", json=ORDER_PAYLOAD)
    assert res.status_code == 400
    assert "Out Of Stock" in res.json()["detail"]


def test_create_order_inventory_not_found(client, mock_collections):
    mock_collections["inventory"].find_one.return_value = None
    res = client.post("/orders", json=ORDER_PAYLOAD)
    assert res.status_code == 404


def test_get_orders(client, mock_collections):
    mock_collections["orders"].find.return_value = [
        {"_id": ObjectId(FAKE_ID), **ORDER_PAYLOAD, "status": "PLACED"}
    ]
    res = client.get("/orders")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_order_found(client, mock_collections):
    mock_collections["orders"].find_one.return_value = {
        "_id": ObjectId(FAKE_ID),
        **ORDER_PAYLOAD,
        "status": "PLACED",
    }
    res = client.get(f"/orders/{FAKE_ID}")
    assert res.status_code == 200
    assert res.json()["status"] == "PLACED"


def test_get_order_not_found(client, mock_collections):
    mock_collections["orders"].find_one.return_value = None
    res = client.get(f"/orders/{FAKE_ID}")
    assert res.status_code == 404


def test_get_order_invalid_id(client, mock_collections):
    res = client.get("/orders/not-an-id")
    assert res.status_code == 400
