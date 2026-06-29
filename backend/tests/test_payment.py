"""Unit tests for payment endpoints."""

from unittest.mock import MagicMock
from bson import ObjectId

FAKE_ID = str(ObjectId())
PAYMENT_PAYLOAD = {"order_id": "order_001", "amount": 99.99}


def test_create_payment_success(client, mock_collections):
    mock_collections["payments"].insert_one.return_value = MagicMock(inserted_id=ObjectId(FAKE_ID))
    res = client.post("/payments", json=PAYMENT_PAYLOAD)
    assert res.status_code == 201
    assert res.json()["status"] == "SUCCESS"
    assert res.json()["payment_id"] == FAKE_ID


def test_get_payments(client, mock_collections):
    mock_collections["payments"].find.return_value = [
        {"_id": ObjectId(FAKE_ID), **PAYMENT_PAYLOAD, "status": "SUCCESS"}
    ]
    res = client.get("/payments")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert res.json()[0]["status"] == "SUCCESS"
