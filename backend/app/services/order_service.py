"""Order business logic — orchestrates inventory check, payment, and order creation."""

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection

from app.exceptions import InvalidObjectIdError, InventoryNotFoundError, OrderNotFoundError, OutOfStockError
from app.logger import get_logger
from app.models.order import Order

logger = get_logger(__name__)


def _parse_id(order_id: str) -> ObjectId:
    try:
        return ObjectId(order_id)
    except (InvalidId, Exception):
        raise InvalidObjectIdError()


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


def create_order(
    order: Order,
    inventory_col: Collection,
    payments_col: Collection,
    orders_col: Collection,
) -> dict:
    """
    Place an order:
    1. Validate inventory exists and has sufficient stock.
    2. Record a SUCCESS payment.
    3. Decrement inventory stock.
    4. Persist the order with PLACED status.
    """
    inventory_item = inventory_col.find_one({"product_id": order.product_id})
    if not inventory_item:
        raise InventoryNotFoundError()
    if inventory_item["stock"] < order.quantity:
        raise OutOfStockError()

    payment = {"order_id": "TEMP", "amount": order.amount, "status": "SUCCESS"}
    payments_col.insert_one(payment)
    logger.info("Payment recorded for order (TEMP) | amount=%.2f", order.amount)

    inventory_col.update_one(
        {"product_id": order.product_id}, {"$inc": {"stock": -order.quantity}}
    )
    logger.info("DB | Inventory decremented for product %s by %d", order.product_id, order.quantity)

    order_data = order.model_dump()
    order_data["status"] = "PLACED"
    result = orders_col.insert_one(order_data)
    logger.info("Order PLACED | order_id=%s user=%s", result.inserted_id, order.user_id)

    return {"message": "Order Created", "order_id": str(result.inserted_id)}


def get_orders(orders_col: Collection) -> list[dict]:
    """Return all orders."""
    return [_serialize(o) for o in orders_col.find()]


def get_order(order_id: str, orders_col: Collection) -> dict:
    """Return a single order by ID or raise OrderNotFoundError."""
    doc = orders_col.find_one({"_id": _parse_id(order_id)})
    if not doc:
        raise OrderNotFoundError()
    return _serialize(doc)
