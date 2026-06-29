"""Inventory business logic."""

from pymongo.collection import Collection

from app.exceptions import InventoryNotFoundError
from app.logger import get_logger
from app.models.inventory import Inventory

logger = get_logger(__name__)


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


def add_inventory(item: Inventory, col: Collection) -> dict:
    """Insert a new inventory record."""
    result = col.insert_one(item.model_dump())
    logger.info("DB | Inventory added for product: %s", item.product_id)
    return {"message": "Inventory Added", "inventory_id": str(result.inserted_id)}


def get_inventory(product_id: str, col: Collection) -> dict:
    """Return inventory for a product or raise InventoryNotFoundError."""
    doc = col.find_one({"product_id": product_id})
    if not doc:
        raise InventoryNotFoundError()
    return _serialize(doc)


def update_inventory(product_id: str, stock: int, col: Collection) -> dict:
    """Set stock level for a product or raise InventoryNotFoundError."""
    result = col.update_one(
        {"product_id": product_id}, {"$set": {"stock": stock}}
    )
    if result.matched_count == 0:
        raise InventoryNotFoundError()
    logger.info("DB | Inventory updated for product %s -> stock=%d", product_id, stock)
    return {"message": "Stock Updated"}
