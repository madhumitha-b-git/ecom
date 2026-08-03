import uuid
from decimal import Decimal
from boto3.dynamodb.conditions import Attr
from database import get_table
from exceptions import ProductNotFoundError
from logger import get_logger
from model import Product


def _to_decimal(item: dict) -> dict:
    """Convert float values to Decimal for DynamoDB compatibility."""
    return {k: Decimal(str(v)) if isinstance(v, float) else v for k, v in item.items()}


def _from_decimal(item: dict) -> dict:
    """Convert Decimal values back to float for JSON response."""
    return {k: float(v) if isinstance(v, Decimal) else v for k, v in item.items()}

logger = get_logger(__name__)


def create_product(product: Product) -> dict:
    product_id = str(uuid.uuid4())
    item = _to_decimal({"product_id": product_id, **product.model_dump()})
    get_table().put_item(Item=item)
    logger.info("DB | Product created: %s", product_id)
    return {"message": "Product Created", "product_id": product_id}


def get_products() -> list[dict]:
    response = get_table().scan()
    return [_from_decimal(i) for i in response.get("Items", [])]


def get_product(product_id: str) -> dict:
    response = get_table().get_item(Key={"product_id": product_id})
    item = response.get("Item")
    if not item:
        raise ProductNotFoundError()
    return _from_decimal(item)


def update_product(product_id: str, product: Product) -> dict:
    existing = get_table().get_item(Key={"product_id": product_id}).get("Item")
    if not existing:
        raise ProductNotFoundError()
    get_table().update_item(
        Key={"product_id": product_id},
        UpdateExpression="SET #n=:n, description=:d, category=:c, price=:p",
        ExpressionAttributeNames={"#n": "name"},
        ExpressionAttributeValues={
            ":n": product.name,
            ":d": product.description,
            ":c": product.category,
            ":p": Decimal(str(product.price)),
        },
    )
    logger.info("DB | Product updated: %s", product_id)
    return {"message": "Product Updated"}


def delete_product(product_id: str) -> dict:
    existing = get_table().get_item(Key={"product_id": product_id}).get("Item")
    if not existing:
        raise ProductNotFoundError()
    get_table().delete_item(Key={"product_id": product_id})
    logger.info("DB | Product deleted: %s", product_id)
    return {"message": "Product Deleted"}
