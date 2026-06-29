"""Cart business logic."""

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection

from app.exceptions import InvalidObjectIdError
from app.logger import get_logger
from app.models.cart import Cart

logger = get_logger(__name__)


def _parse_id(cart_id: str) -> ObjectId:
    try:
        return ObjectId(cart_id)
    except (InvalidId, Exception):
        raise InvalidObjectIdError()


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


def add_to_cart(item: Cart, col: Collection) -> dict:
    """Add an item to the cart."""
    result = col.insert_one(item.model_dump())
    logger.info("DB | Cart item added for user: %s", item.user_id)
    return {"message": "Added To Cart", "cart_id": str(result.inserted_id)}


def get_cart(user_id: str, col: Collection) -> list[dict]:
    """Return all cart items for a user."""
    return [_serialize(item) for item in col.find({"user_id": user_id})]


def delete_cart_item(cart_id: str, col: Collection) -> dict:
    """Remove a single cart item by ID."""
    col.delete_one({"_id": _parse_id(cart_id)})
    logger.info("DB | Cart item deleted: %s", cart_id)
    return {"message": "Cart Item Deleted"}
