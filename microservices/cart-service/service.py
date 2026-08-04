import uuid
import httpx
from boto3.dynamodb.conditions import Attr
from database import get_table
from exceptions import CartItemNotFoundError, ProductNotFoundError
from logger import get_logger
from model import Cart
from config import settings

logger = get_logger(__name__)


from urllib.parse import quote

def _validate_product(product_id: str) -> None:
    try:
        safe_product_id = quote(product_id)
        resp = httpx.get(f"{settings.PRODUCT_SERVICE_URL}/v1/products/{safe_product_id}", timeout=5.0)
        if resp.status_code == 404:
            raise ProductNotFoundError()
        resp.raise_for_status()
    except httpx.RequestError:
        logger.error("HTTP | Product service unreachable")
        raise ProductNotFoundError()


def _publish_analytics_event(event_type: str, data: dict):
    try:
        httpx.post("http://localhost:8005/v1/analytics/publish-event", json={
            "event_type": event_type,
            "data": data
        }, timeout=1.0)
    except Exception as e:
        logger.warning("Analytics | Failed to publish event: %s", e)


def add_to_cart(item: Cart) -> dict:
    _validate_product(item.product_id)
    cart_id = str(uuid.uuid4())
    get_table().put_item(Item={"cart_id": cart_id, **item.model_dump()})
    logger.info("DB | Cart item added: user=%s product=%s", item.user_id, item.product_id)
    
    _publish_analytics_event("cart_action", {
        "action": "add",
        "user_id": item.user_id,
        "product_id": item.product_id,
        "quantity": item.quantity
    })
    
    return {"message": "Added To Cart", "cart_id": cart_id}


def get_cart(user_id: str) -> list[dict]:
    response = get_table().scan(FilterExpression=Attr("user_id").eq(user_id))
    return response.get("Items", [])


def delete_cart_item(cart_id: str) -> dict:
    existing = get_table().get_item(Key={"cart_id": cart_id}).get("Item")
    if not existing:
        raise CartItemNotFoundError()
    get_table().delete_item(Key={"cart_id": cart_id})
    logger.info("DB | Cart item deleted: %s", cart_id)
    
    _publish_analytics_event("cart_action", {
        "action": "remove",
        "user_id": existing.get("user_id"),
        "product_id": existing.get("product_id")
    })
    
    return {"message": "Cart Item Deleted"}


def clear_user_cart(user_id: str) -> dict:
    items = get_cart(user_id)
    with get_table().batch_writer() as batch:
        for item in items:
            batch.delete_item(Key={"cart_id": item["cart_id"]})
    logger.info("DB | Cart cleared for user: %s (%d items)", user_id, len(items))
    
    _publish_analytics_event("cart_action", {
        "action": "clear",
        "user_id": user_id
    })
    
    return {"message": "Cart Cleared", "items_removed": len(items)}
