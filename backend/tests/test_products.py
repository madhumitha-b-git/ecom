"""Unit tests for product endpoints."""

from unittest.mock import MagicMock
from bson import ObjectId

PRODUCT_PAYLOAD = {
    "name": "Headphones",
    "description": "Wireless",
    "category": "Electronics",
    "price": 49.99,
}
FAKE_ID = str(ObjectId())


def test_create_product(client, mock_collections):
    mock_collections["products"].insert_one.return_value = MagicMock(inserted_id=ObjectId(FAKE_ID))
    res = client.post("/products", json=PRODUCT_PAYLOAD)
    assert res.status_code == 201
    assert res.json()["product_id"] == FAKE_ID


def test_get_products(client, mock_collections):
    mock_collections["products"].find.return_value = [
        {"_id": ObjectId(FAKE_ID), **PRODUCT_PAYLOAD}
    ]
    res = client.get("/products")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_get_product_found(client, mock_collections):
    mock_collections["products"].find_one.return_value = {"_id": ObjectId(FAKE_ID), **PRODUCT_PAYLOAD}
    res = client.get(f"/products/{FAKE_ID}")
    assert res.status_code == 200
    assert res.json()["name"] == "Headphones"


def test_get_product_not_found(client, mock_collections):
    mock_collections["products"].find_one.return_value = None
    res = client.get(f"/products/{FAKE_ID}")
    assert res.status_code == 404


def test_get_product_invalid_id(client, mock_collections):
    res = client.get("/products/invalid-id")
    assert res.status_code == 400


def test_update_product(client, mock_collections):
    mock_collections["products"].update_one.return_value = MagicMock(matched_count=1)
    res = client.put(f"/products/{FAKE_ID}", json=PRODUCT_PAYLOAD)
    assert res.status_code == 200
    assert res.json()["message"] == "Product Updated"


def test_update_product_not_found(client, mock_collections):
    mock_collections["products"].update_one.return_value = MagicMock(matched_count=0)
    res = client.put(f"/products/{FAKE_ID}", json=PRODUCT_PAYLOAD)
    assert res.status_code == 404


def test_delete_product(client, mock_collections):
    mock_collections["products"].delete_one.return_value = MagicMock(deleted_count=1)
    res = client.delete(f"/products/{FAKE_ID}")
    assert res.status_code == 200
    assert res.json()["message"] == "Product Deleted"


def test_delete_product_not_found(client, mock_collections):
    mock_collections["products"].delete_one.return_value = MagicMock(deleted_count=0)
    res = client.delete(f"/products/{FAKE_ID}")
    assert res.status_code == 404
