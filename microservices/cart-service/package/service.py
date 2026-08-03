import uuid
from boto3.dynamodb.conditions import Attr
from database import get_table
from exceptions import CartItemNotFoundError
from logger import get_logger
from model import Cart

logger = get_logger(__name__)


def add_to_cart(item: Cart) -> dict:
    cart_id = str(uuid.uuid4())
    get_table().put_item(Item={"cart_id": cart_id, **item.model_dump()})
    logger.info("DB | Cart item added: user=%s product=%s", item.user_id, item.product_id)
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
    return {"message": "Cart Item Deleted"}
