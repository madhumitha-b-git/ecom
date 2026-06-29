"""Unit tests for cart endpoints."""

from unittest.mock import MagicMock
from bson import ObjectId

FAKE_ID = str(ObjectId())
CART_PAYLOAD = {"user_id": "user1", "product_id": "prod_001", "quantity": 2}


def test_add_to_cart(client, mock_collections):
    mock_collections["cart"].insert_one.return_value = MagicMock(inserted_id=ObjectId(FAKE_ID))
    res = client.post("/cart", json=CART_PAYLOAD)
    assert res.status_code == 201
    assert res.json()["cart_id"] == FAKE_ID


def test_get_cart(client, mock_collections):
    mock_collections["cart"].find.return_value = [
        {"_id": ObjectId(FAKE_ID), **CART_PAYLOAD}
    ]
    res = client.get("/cart/user1")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_cart_empty(client, mock_collections):
    mock_collections["cart"].find.return_value = []
    res = client.get("/cart/user_nobody")
    assert res.status_code == 200
    assert res.json() == []


def test_delete_cart_item(client, mock_collections):
    mock_collections["cart"].delete_one.return_value = MagicMock()
    res = client.delete(f"/cart/{FAKE_ID}")
    assert res.status_code == 200
    assert res.json()["message"] == "Cart Item Deleted"


def test_delete_cart_item_invalid_id(client, mock_collections):
    res = client.delete("/cart/bad-id")
    assert res.status_code == 400
