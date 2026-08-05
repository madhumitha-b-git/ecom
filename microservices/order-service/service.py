import uuid
import json
import boto3
import httpx
from decimal import Decimal
from database import get_table
from exceptions import InventoryNotFoundError, OrderNotFoundError, OutOfStockError, PaymentFailedError
from logger import get_logger
from model import Order
from config import settings

logger = get_logger(__name__)

sns = None
try:
    if getattr(settings, "AWS_PROFILE", None):
        session = boto3.Session(profile_name=settings.AWS_PROFILE)
        sns = session.client("sns", region_name=settings.AWS_REGION)
    else:
        sns = boto3.client("sns", region_name=settings.AWS_REGION)
except Exception as e:
    logger.warning("SNS | Failed to initialize SNS client: %s. Using local HTTP triggers fallback.", e)

ORDER_CREATED_TOPIC_ARN = "arn:aws:sns:ap-southeast-1:726101441380:order-event_ecom"


def _to_decimal(item: dict) -> dict:
    return {k: Decimal(str(v)) if isinstance(v, float) else v for k, v in item.items()}


def _from_decimal(item: dict) -> dict:
    return {k: float(v) if isinstance(v, Decimal) else v for k, v in item.items()}


from urllib.parse import quote

def _call_inventory_decrement(product_id: str, quantity: int) -> None:
    """Call inventory-service over HTTP to decrement stock. (Kept for reference / rollback; no longer called from create_order.)"""
    safe_product_id = quote(product_id)
    url = f"{settings.INVENTORY_SERVICE_URL}/v1/inventory/{safe_product_id}/decrement"
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
    if sns is None:
        raise Exception("SNS client is not initialized")
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


def _publish_analytics_event(event_type: str, data: dict):
    import os
    analytics_url = os.environ.get("ANALYTICS_SERVICE_URL", "http://localhost:8005")
    try:
        httpx.post(f"{analytics_url}/v1/analytics/publish-event", json={
            "event_type": event_type,
            "data": data
        }, timeout=1.0)
    except Exception as e:
        logger.warning("Analytics | Failed to publish event: %s", e)


def create_order(order: Order) -> dict:
    """
    Synchronous order fulfillment pipeline:
    1. Check stock. Raise OutOfStockError if not enough.
    2. Decrement stock.
    3. Process payment.
    4. Save order to database (SUCCESS or FAILED).
    5. Trigger analytics update event.
    """
    import datetime
    from urllib.parse import quote
    order_id = "order-" + str(uuid.uuid4())[:8]
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    safe_product_id = quote(order.product_id)

    # A. Check stock level first
    stock_url = f"{settings.INVENTORY_SERVICE_URL}/v1/inventory/{safe_product_id}"
    try:
        stock_resp = httpx.get(stock_url, timeout=5.0)
        if stock_resp.status_code == 404:
            raise InventoryNotFoundError()
        stock_resp.raise_for_status()
        stock_data = stock_resp.json()
        current_stock = int(stock_data.get("stock", 0))
        if current_stock < order.quantity:
            logger.warning("OrderFailed | Insufficient stock: product=%s, available=%d, requested=%d", order.product_id, current_stock, order.quantity)
            raise OutOfStockError()
    except httpx.RequestError as e:
        logger.error("Inventory service unreachable for stock check: %s", e)
        raise InventoryNotFoundError()

    # B. Decrement stock level
    inv_url = f"{settings.INVENTORY_SERVICE_URL}/v1/inventory/{safe_product_id}/decrement"
    try:
        inv_resp = httpx.post(inv_url, params={"quantity": order.quantity}, timeout=5.0)
        if inv_resp.status_code != 200:
            logger.warning("OrderFailed | Stock decrement rejected: %s", inv_resp.status_code)
            raise OutOfStockError()
    except Exception as e:
        logger.error("Error during stock decrement: %s", e)
        raise OutOfStockError()

    # C. Charge payment
    pay_url = f"{settings.PAYMENT_SERVICE_URL}/v1/payments"
    payment_success = False
    try:
        pay_resp = httpx.post(pay_url, json={"order_id": order_id, "amount": float(order.amount)}, timeout=5.0)
        if pay_resp.status_code == 201:
            payment_success = True
        else:
            logger.warning("OrderFailed | Payment service rejected charge: %s", pay_resp.status_code)
    except Exception as e:
        logger.error("Error processing payment: %s", e)

    if not payment_success:
        # Rollback stock decrement (compensating transaction)
        logger.info("LocalPipeline | Rolling back stock decrement for order: %s", order_id)
        try:
            # Restore stock by resetting to original level
            httpx.put(f"{settings.INVENTORY_SERVICE_URL}/v1/inventory/{safe_product_id}", params={"stock": current_stock}, timeout=5.0)
        except Exception as rollback_err:
            logger.error("LocalPipeline | Failed to rollback stock decrement: %s", rollback_err)

        # Save order as FAILED
        item = _to_decimal({"order_id": order_id, **order.model_dump(), "status": "FAILED", "timestamp": timestamp})
        get_table().put_item(Item=item)
        _publish_analytics_event("order_status_update", {
            "order_id": order_id,
            "status": "FAILED",
            "product_id": order.product_id,
            "user_id": order.user_id,
            "amount": float(order.amount),
            "quantity": order.quantity
        })
        raise PaymentFailedError()

    # Success path
    item = _to_decimal({"order_id": order_id, **order.model_dump(), "status": "SUCCESS", "timestamp": timestamp})
    get_table().put_item(Item=item)
    
    # Publish status updates to analytics
    _publish_analytics_event("order_status_update", {
        "order_id": order_id,
        "status": "SUCCESS",
        "product_id": order.product_id,
        "user_id": order.user_id,
        "amount": float(order.amount),
        "quantity": order.quantity
    })
    
    logger.info("Order SUCCESS | order_id=%s user=%s", order_id, order.user_id)
    return {"message": "Order Created", "order_id": order_id, "status": "SUCCESS"}


def get_orders() -> list[dict]:
    return [_from_decimal(i) for i in get_table().scan().get("Items", [])]


def get_orders_for_user(username: str) -> list[dict]:
    all_orders = get_orders()
    return [o for o in all_orders if o.get("user_id") == username]


def get_order(order_id: str) -> dict:
    item = get_table().get_item(Key={"order_id": order_id}).get("Item")
    if not item:
        raise OrderNotFoundError()
    return _from_decimal(item)


def update_order_status(order_id: str, status: str) -> dict:
    existing = get_table().get_item(Key={"order_id": order_id}).get("Item")
    if not existing:
        raise OrderNotFoundError()
    get_table().update_item(
        Key={"order_id": order_id},
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": status},
    )
    logger.info("DB | Order status updated: order_id=%s status=%s", order_id, status)

    # Publish status update event to analytics service
    event_data = {
        "order_id": order_id,
        "status": status,
        "product_id": existing.get("product_id"),
        "user_id": existing.get("user_id"),
        "amount": float(existing.get("amount", 0.0)),
        "quantity": int(existing.get("quantity", 1))
    }
    _publish_analytics_event("order_status_update", event_data)

    return {"message": "Order Status Updated", "order_id": order_id, "status": status}