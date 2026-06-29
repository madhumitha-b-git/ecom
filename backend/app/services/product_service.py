"""Product CRUD business logic."""

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection

from app.exceptions import InvalidObjectIdError, ProductNotFoundError
from app.logger import get_logger
from app.models.product import Product

logger = get_logger(__name__)


def _parse_id(product_id: str) -> ObjectId:
    try:
        return ObjectId(product_id)
    except (InvalidId, Exception):
        raise InvalidObjectIdError()


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


def create_product(product: Product, col: Collection) -> dict:
    """Insert a new product and return its ID."""
    result = col.insert_one(product.model_dump())
    logger.info("DB | Product created: %s", result.inserted_id)
    return {"message": "Product Created", "product_id": str(result.inserted_id)}


def get_products(col: Collection) -> list[dict]:
    """Return all products."""
    return [_serialize(p) for p in col.find()]


def get_product(product_id: str, col: Collection) -> dict:
    """Return a single product by ID or raise ProductNotFoundError."""
    doc = col.find_one({"_id": _parse_id(product_id)})
    if not doc:
        raise ProductNotFoundError()
    return _serialize(doc)


def update_product(product_id: str, product: Product, col: Collection) -> dict:
    """Update a product by ID or raise ProductNotFoundError."""
    result = col.update_one(
        {"_id": _parse_id(product_id)}, {"$set": product.model_dump()}
    )
    if result.matched_count == 0:
        raise ProductNotFoundError()
    logger.info("DB | Product updated: %s", product_id)
    return {"message": "Product Updated"}


def delete_product(product_id: str, col: Collection) -> dict:
    """Delete a product by ID or raise ProductNotFoundError."""
    result = col.delete_one({"_id": _parse_id(product_id)})
    if result.deleted_count == 0:
        raise ProductNotFoundError()
    logger.info("DB | Product deleted: %s", product_id)
    return {"message": "Product Deleted"}
