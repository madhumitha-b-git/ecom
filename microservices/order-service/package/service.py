import uuid
import json
import boto3
import httpx
from decimal import Decimal
from database import get_table
from exceptions import InventoryNotFoundError, OrderNotFoundError, OutOfStockError
from logger import get_logger
from model import Order
from config import settings

logger = get_logger(__name__)

sns = boto3.client("sns", region_name=settings.AWS_REGION)
ORDER_CREATED_TOPIC_ARN = "arn:aws:sns:ap-southeast-1:726101441380:order-event_ecom"


def _to_decimal(item: dict) -> dict:
    return {k: Decimal(str(v)) if isinstance(v, float) else v for k, v in item.items()}


def _from_decimal(item: dict) -> dict:
    return {k: float(v) if isinstance(v, Decimal) else v for k, v in item.items()}


def _call_inventory_decrement(product_id: str, quantity: int) -> None:
    """Call inventory-service over HTTP to decrement stock. (Kept for reference / rollback; no longer called from create_order.)"""
    url = f"{settings.INVENTORY_SERVICE_URL}/inventory/{product_id}/decrement"
    try:
        response = httpx.post(url, params={"quantity": quantity}, timeout=5.0)
    except httpx.RequestError as e:
        logger.error("Inventory service unreachable: %s", e)
        raise InventoryNotFoundError()
    if response.status_code == 404:
        raise InventoryNotFoundError()
    if response.status_code == 400:
        raise OutOfStockError()
    response.raise_for_status()
    logger.info("Inventory decremented via HTTP: product=%s qty=%d", product_id, quantity)


def _publish_order_created(order_id: str, product_id: str, quantity: int, amount: float, user_id: str) -> None:
    """Publish an OrderCreated event to SNS for inventory-service to consume."""
    sns.publish(
        TopicArn=ORDER_CREATED_TOPIC_ARN,
        Message=json.dumps({
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "amount": amount,
            "user_id": user_id,
        }),
    )
    logger.info("OrderCreated event published: order_id=%s product=%s qty=%d", order_id, product_id, quantity)


def _call_payment_create(order_id: str, amount: float) -> str:
    """Call payment-service over HTTP to record a payment. (Kept for reference; no longer called from create_order.)"""
    url = f"{settings.PAYMENT_SERVICE_URL}/payments"
    try:
        response = httpx.post(url, json={"order_id": order_id, "amount": amount}, timeout=5.0)
        response.raise_for_status()
    except httpx.RequestError as e:
        logger.error("Payment service unreachable: %s", e)
        raise
    data = response.json()
    logger.info("Payment recorded via HTTP: payment_id=%s", data.get("payment_id"))
    return data["payment_id"]


def create_order(order: Order) -> dict:
    """
    1. Publish OrderCreated event to SNS (async) for inventory-service to reserve stock.
    2. Payment is now handled asynchronously: inventory-service publishes
       InventoryReserved -> payment-service consumes it and processes payment.
       order-service no longer calls payment-service directly.
    3. Persist order in own DynamoDB table with status PENDING.
    """
    order_id = str(uuid.uuid4())

    _publish_order_created(order_id, order.product_id, order.quantity, order.amount, order.user_id)

    item = _to_decimal({"order_id": order_id, **order.model_dump(), "status": "PENDING"})
    get_table().put_item(Item=item)
    logger.info("Order PENDING | order_id=%s user=%s", order_id, order.user_id)
    return {"message": "Order Created", "order_id": order_id}


def get_orders() -> list[dict]:
    return [_from_decimal(i) for i in get_table().scan().get("Items", [])]


def get_order(order_id: str) -> dict:
    item = get_table().get_item(Key={"order_id": order_id}).get("Item")
    if not item:
        raise OrderNotFoundError()
    return _from_decimal(item)