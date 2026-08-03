import uuid
from decimal import Decimal
from database import get_table
from exceptions import PaymentFailureError
from logger import get_logger
from model import Payment

logger = get_logger(__name__)


def _to_decimal(item: dict) -> dict:
    return {k: Decimal(str(v)) if isinstance(v, float) else v for k, v in item.items()}


def _from_decimal(item: dict) -> dict:
    return {k: float(v) if isinstance(v, Decimal) else v for k, v in item.items()}


def create_payment(payment: Payment) -> dict:
    payment_id = str(uuid.uuid4())
    item = _to_decimal({"payment_id": payment_id, **payment.model_dump(), "status": "SUCCESS"})
    get_table().put_item(Item=item)
    logger.info("Payment SUCCESS | payment_id=%s order_id=%s", payment_id, payment.order_id)
    return {"payment_id": payment_id, "status": "SUCCESS"}


def get_payments() -> list[dict]:
    return [_from_decimal(i) for i in get_table().scan().get("Items", [])]
