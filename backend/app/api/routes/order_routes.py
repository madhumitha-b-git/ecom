"""Order endpoints."""

from fastapi import APIRouter, Depends
from pymongo.collection import Collection

from app.dependencies import inventory_col, orders_col, payments_col
from app.logger import get_logger
from app.models.order import Order
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])
logger = get_logger(__name__)


@router.post(
    "",
    status_code=201,
    summary="Place an order",
    description="Validates inventory, processes payment, decrements stock, and creates the order.",
    responses={
        400: {"description": "Out of stock"},
        404: {"description": "Inventory not found"},
        402: {"description": "Payment failed"},
    },
)
def create_order(
    order: Order,
    inv_col: Collection = Depends(inventory_col),
    pay_col: Collection = Depends(payments_col),
    ord_col: Collection = Depends(orders_col),
):
    logger.info("POST /orders | user=%s product=%s qty=%d", order.user_id, order.product_id, order.quantity)
    return order_service.create_order(order, inv_col, pay_col, ord_col)


@router.get(
    "",
    summary="List all orders",
    description="Retrieve every order placed in the system.",
)
def get_orders(ord_col: Collection = Depends(orders_col)):
    logger.info("GET /orders")
    return order_service.get_orders(ord_col)


@router.get(
    "/{order_id}",
    summary="Get an order",
    description="Retrieve a single order by its MongoDB ObjectId.",
    responses={400: {"description": "Invalid ID"}, 404: {"description": "Order not found"}},
)
def get_order(order_id: str, ord_col: Collection = Depends(orders_col)):
    logger.info("GET /orders/%s", order_id)
    return order_service.get_order(order_id, ord_col)
