import httpx
from decimal import Decimal
from database import get_table
from exceptions import InventoryNotFoundError, OutOfStockError, ProductNotFoundError
from logger import get_logger
from model import Inventory
from config import settings

logger = get_logger(__name__)


from urllib.parse import quote

def _get_product(product_id: str) -> dict | None:
    try:
        safe_product_id = quote(product_id)
        resp = httpx.get(f"{settings.PRODUCT_SERVICE_URL}/v1/products/{safe_product_id}", timeout=5.0)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()
    except httpx.RequestError as e:
        logger.error("HTTP | Failed to call product service: %s", e)
        raise ProductNotFoundError()


def _format_inventory(item: dict) -> dict:
    pid = item.get("inventory_id") or item.get("product_id", "")
    product = _get_product(pid) if pid else None
    return {
        "product_id": pid,
        "stock": int(item["stock"]),
        "product": product,
    }


def add_inventory(item: Inventory) -> dict:
    product = _get_product(item.product_id)
    if not product:
        raise ProductNotFoundError()
    # Key is inventory_id to match DynamoDB partition key
    get_table().put_item(Item={"inventory_id": item.product_id, "product_id": item.product_id, "stock": item.stock})
    logger.info("DB | Inventory added: product_id=%s stock=%d", item.product_id, item.stock)
    return {"message": "Inventory Added", "product_id": item.product_id}


def get_inventory(product_id: str) -> dict:
    response = get_table().get_item(Key={"inventory_id": product_id})
    item = response.get("Item")
    if not item:
        raise InventoryNotFoundError()
    return _format_inventory(item)


def update_inventory(product_id: str, stock: int) -> dict:
    existing = get_table().get_item(Key={"inventory_id": product_id}).get("Item")
    if not existing:
        raise InventoryNotFoundError()
    get_table().update_item(
        Key={"inventory_id": product_id},
        UpdateExpression="SET stock = :s",
        ExpressionAttributeValues={":s": stock},
    )
    logger.info("DB | Stock updated: product_id=%s stock=%d", product_id, stock)
    return {"message": "Stock Updated"}


def get_all_inventory() -> list[dict]:
    response = get_table().scan()
    items = response.get("Items", [])
    return [_format_inventory(item) for item in items]


def decrement_stock(product_id: str, quantity: int) -> dict:
    """Called internally by order-service via HTTP. Raises OutOfStockError if insufficient."""
    item = get_table().get_item(Key={"inventory_id": product_id}).get("Item")
    if not item:
        raise InventoryNotFoundError()
    current = int(item["stock"])
    if current < quantity:
        raise OutOfStockError()
    get_table().update_item(
        Key={"inventory_id": product_id},
        UpdateExpression="SET stock = stock - :q",
        ConditionExpression="stock >= :q",
        ExpressionAttributeValues={":q": quantity},
    )
    logger.info("DB | Stock decremented: product_id=%s by=%d", product_id, quantity)
    return {"message": "Stock Decremented", "product_id": product_id, "remaining": current - quantity}
