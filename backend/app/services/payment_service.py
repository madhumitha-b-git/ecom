"""Payment business logic."""

from pymongo.collection import Collection

from app.logger import get_logger
from app.models.payment import Payment

logger = get_logger(__name__)


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


def create_payment(payment: Payment, col: Collection) -> dict:
    """Process a payment and persist it with SUCCESS status."""
    data = payment.model_dump()
    data["status"] = "SUCCESS"
    result = col.insert_one(data)
    logger.info("Payment SUCCESS | payment_id=%s order_id=%s", result.inserted_id, payment.order_id)
    return {"payment_id": str(result.inserted_id), "status": "SUCCESS"}


def get_payments(col: Collection) -> list[dict]:
    """Return all payment records."""
    return [_serialize(p) for p in col.find()]
