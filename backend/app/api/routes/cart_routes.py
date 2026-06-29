"""Cart endpoints."""

from fastapi import APIRouter, Depends
from pymongo.collection import Collection

from app.dependencies import cart_col
from app.logger import get_logger
from app.models.cart import Cart
from app.services import cart_service

router = APIRouter(prefix="/cart", tags=["Cart"])
logger = get_logger(__name__)


@router.post(
    "",
    status_code=201,
    summary="Add to cart",
    description="Add a product item to a user's cart.",
)
def add_to_cart(item: Cart, col: Collection = Depends(cart_col)):
    logger.info("POST /cart | user=%s product=%s qty=%d", item.user_id, item.product_id, item.quantity)
    return cart_service.add_to_cart(item, col)


@router.get(
    "/{user_id}",
    summary="Get cart",
    description="Retrieve all cart items belonging to a user.",
)
def get_cart(user_id: str, col: Collection = Depends(cart_col)):
    logger.info("GET /cart/%s", user_id)
    return cart_service.get_cart(user_id, col)


@router.delete(
    "/{cart_id}",
    summary="Remove cart item",
    description="Delete a specific item from the cart by cart entry ID.",
    responses={400: {"description": "Invalid ID"}},
)
def delete_cart_item(cart_id: str, col: Collection = Depends(cart_col)):
    logger.info("DELETE /cart/%s", cart_id)
    return cart_service.delete_cart_item(cart_id, col)
