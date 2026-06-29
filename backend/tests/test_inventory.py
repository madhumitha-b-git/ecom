"""Unit tests for inventory endpoints."""

from unittest.mock import MagicMock
from bson import ObjectId

FAKE_ID = str(ObjectId())
PRODUCT_ID = "prod_001"


def test_add_inventory(client, mock_collections):
    mock_collections["inventory"].insert_one.return_value = MagicMock(inserted_id=ObjectId(FAKE_ID))
    res = client.post("/inventory", json={"product_id": PRODUCT_ID, "stock": 50})
    assert res.status_code == 201
    assert "inventory_id" in res.json()


def test_get_inventory(client, mock_collections):
    mock_collections["inventory"].find_one.return_value = {
        "_id": ObjectId(FAKE_ID),
        "product_id": PRODUCT_ID,
        "stock": 50,
    }
    res = client.get(f"/inventory/{PRODUCT_ID}")
    assert res.status_code == 200
    assert res.json()["stock"] == 50


def test_get_inventory_not_found(client, mock_collections):
    mock_collections["inventory"].find_one.return_value = None
    res = client.get(f"/inventory/{PRODUCT_ID}")
    assert res.status_code == 404


def test_update_stock(client, mock_collections):
    mock_collections["inventory"].update_one.return_value = MagicMock(matched_count=1)
    res = client.put(f"/inventory/{PRODUCT_ID}?stock=100")
    assert res.status_code == 200
    assert res.json()["message"] == "Stock Updated"


def test_update_stock_out_of_range(client, mock_collections):
    """Negative stock should fail validation."""
    res = client.put(f"/inventory/{PRODUCT_ID}?stock=-1")
    assert res.status_code == 422


def test_update_stock_not_found(client, mock_collections):
    mock_collections["inventory"].update_one.return_value = MagicMock(matched_count=0)
    res = client.put(f"/inventory/{PRODUCT_ID}?stock=10")
    assert res.status_code == 404
