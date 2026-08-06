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

def _get_account_id() -> str:
    try:
        if getattr(settings, "AWS_PROFILE", None):
            session = boto3.Session(profile_name=settings.AWS_PROFILE)
            return session.client("sts").get_caller_identity()["Account"]
        return boto3.client("sts").get_caller_identity()["Account"]
    except Exception:
        return "726101441380"

ORDER_CREATED_TOPIC_ARN = f"arn:aws:sns:{settings.AWS_REGION}:{_get_account_id()}:order-event_ecom"


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
    1. Persist order in own DynamoDB table with status PENDING.
    2. Try to publish OrderCreated event to SNS (async).
    3. Fallback to direct HTTP synchronous validation if offline.
    """
    import datetime
    order_id = "order-" + str(uuid.uuid4())[:8]
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    item = _to_decimal({"order_id": order_id, **order.model_dump(), "status": "PENDING", "timestamp": timestamp})
    get_table().put_item(Item=item)
    logger.info("Order PENDING | order_id=%s user=%s", order_id, order.user_id)

    # Publish initial PENDING status event to analytics
    _publish_analytics_event("order_status_update", {
        "order_id": order_id,
        "status": "PENDING",
        "product_id": order.product_id,
        "user_id": order.user_id,
        "amount": float(order.amount),
        "quantity": order.quantity
    })

    # Try to publish via AWS SNS (live cloud async event flow)
    sns_success = False
    try:
        _publish_order_created(order_id, order.product_id, order.quantity, order.amount, order.user_id)
        sns_success = True
    except Exception as e:
        logger.warning("SNS | Failed to publish OrderCreated event: %s. Falling back to local HTTP pipeline...", e)

    # Local fallback verification trigger
    use_local_fallback = not sns_success or type(get_table()).__name__ == "LocalOrderDB"
    if use_local_fallback:
        import threading
        import time
        
        def run_local_pipeline():
            time.sleep(1.0)  # Simulated validation latency delay
            try:
                # Step A: Decrement inventory stock over HTTP
                headers = {"Authorization": "Bearer dXNlcjEyMzoxNzIwMDAwMDAw"}
                inv_url = f"{settings.INVENTORY_SERVICE_URL}/v1/inventory/{order.product_id}/decrement"
                logger.info("LocalPipeline | Requesting stock decrement at: %s", inv_url)
                inv_resp = httpx.post(inv_url, params={"quantity": order.quantity}, headers=headers, timeout=5.0)
                
                if inv_resp.status_code != 200:
                    logger.warning("LocalPipeline | Stock reservation failed for product: %s, response: %s", order.product_id, inv_resp.status_code)
                    update_order_status(order_id, "INVENTORY_FAILED")
                    return
                
                _publish_analytics_event("order_status_update", {
                    "order_id": order_id,
                    "status": "INVENTORY_RESERVED",
                    "product_id": order.product_id,
                    "user_id": order.user_id,
                    "amount": float(order.amount),
                    "quantity": order.quantity
                })

                # Step B: Record payment over HTTP
                pay_url = f"{settings.PAYMENT_SERVICE_URL}/v1/payments"
                logger.info("LocalPipeline | Requesting payment charge at: %s", pay_url)
                pay_resp = httpx.post(pay_url, json={"order_id": order_id, "amount": float(order.amount)}, headers=headers, timeout=5.0)
                
                if pay_resp.status_code != 201:
                    logger.warning("LocalPipeline | Payment failed for order: %s, response: %s", order_id, pay_resp.status_code)
                    update_order_status(order_id, "FAILED")
                    return

                # Success
                update_order_status(order_id, "SUCCESS")
                logger.info("LocalPipeline | Order verification succeeded for order_id: %s", order_id)

            except Exception as ex:
                logger.error("LocalPipeline | Error running local verification pipeline: %s", ex)
                update_order_status(order_id, "FAILED")

        threading.Thread(target=run_local_pipeline).start()

    return {"message": "Order Created", "order_id": order_id}


def get_orders() -> list[dict]:
    return [_from_decimal(i) for i in get_table().scan().get("Items", [])]


def get_orders_for_user(username: str) -> list[dict]:
    all_orders = get_orders()
    return [o for o in all_orders if str(o.get("user_id")).strip().lower() == username.strip().lower()]


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