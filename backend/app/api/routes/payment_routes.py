"""Payment endpoints."""

from fastapi import APIRouter, Depends
from pymongo.collection import Collection

from app.dependencies import payments_col
from app.logger import get_logger
from app.models.payment import Payment
from app.services import payment_service

router = APIRouter(prefix="/payments", tags=["Payments"])
logger = get_logger(__name__)


@router.post(
    "",
    status_code=201,
    summary="Create payment",
    description="Process a payment for an order. Returns SUCCESS status on completion.",
    responses={402: {"description": "Payment failed"}},
)
def create_payment(payment: Payment, col: Collection = Depends(payments_col)):
    logger.info("POST /payments | order_id=%s amount=%.2f", payment.order_id, payment.amount)
    return payment_service.create_payment(payment, col)


@router.get(
    "",
    summary="List payments",
    description="Retrieve all payment records.",
)
def get_payments(col: Collection = Depends(payments_col)):
    logger.info("GET /payments")
    return payment_service.get_payments(col)
