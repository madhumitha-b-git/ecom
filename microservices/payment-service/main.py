from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.fastapi.middleware import FastAPIMiddleware
patch_all()

import json
import httpx
from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from exceptions import register_handlers
from logger import get_logger
from model import Payment
from auth import verify_jwt_token
from config import settings
import service

logger = get_logger(__name__)
app = FastAPI(title="Payment Service", version="1.0.0")
app.add_middleware(FastAPIMiddleware, recorder=xray_recorder)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
register_handlers(app)

router = APIRouter()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("--> %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("<-- %s %s %d", request.method, request.url.path, response.status_code)
    return response


@app.get("/", tags=["Health"])
def health():
    return {"service": "payment-service", "status": "ok"}


@router.post("/payments", status_code=201, summary="Process payment")
def create_payment(payment: Payment, username: str = Depends(verify_jwt_token)):
    return service.create_payment(payment)


@router.get("/payments", summary="List all payments")
def get_payments(username: str = Depends(verify_jwt_token)):
    return service.get_payments()

app.include_router(router, prefix="/v1")


# API Gateway entry point (unchanged)
api_handler = Mangum(app)


def _process_inventory_result(message: dict) -> None:
    """Handle InventoryReserved/InventoryFailed: only charge payment if inventory was reserved."""
    order_id = message["order_id"]
    status = message.get("status")
    amount = message.get("amount", 0)

    if status != "RESERVED":
        logger.info("SQS | Skipping payment for order_id=%s (inventory status=%s)", order_id, status)
        return

    logger.info("SQS | Processing payment for order_id=%s amount=%s", order_id, amount)
    payment = Payment(order_id=order_id, amount=amount)
    
    try:
        service.create_payment(payment)
        logger.info("SQS | Payment processed for order_id=%s", order_id)
        # Call order-service to mark as SUCCESS
        httpx.put(f"{settings.ORDER_SERVICE_URL}/v1/orders/{order_id}/status", params={"status": "SUCCESS"}, timeout=5.0)
        logger.info("HTTP | Marked order status as SUCCESS for order_id=%s", order_id)
    except Exception as e:
        logger.error("SQS | Payment failure for order_id=%s: %s", order_id, e)
        # Call order-service to mark as FAILED
        try:
            httpx.put(f"{settings.ORDER_SERVICE_URL}/v1/orders/{order_id}/status", params={"status": "FAILED"}, timeout=5.0)
            logger.info("HTTP | Marked order status as FAILED for order_id=%s due to payment failure", order_id)
        except Exception as http_err:
            logger.error("HTTP | Failed to mark order status as FAILED: %s", http_err)


def handler(event, context):
    """
    Unified Lambda entry point.
    - If triggered by SQS (event has 'Records'), process each InventoryReserved/Failed message.
    - Otherwise, treat it as an API Gateway event and delegate to Mangum/FastAPI.
    """
    if "Records" in event:
        for record in event["Records"]:
            sns_envelope = json.loads(record["body"])
            message = json.loads(sns_envelope["Message"])
            try:
                _process_inventory_result(message)
            except Exception as e:
                logger.error("SQS | Failed to process record: %s", e)
                raise
        return {"status": "processed"}

    # Not an SQS event -> API Gateway request
    return api_handler(event, context)