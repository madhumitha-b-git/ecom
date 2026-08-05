from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.fastapi.middleware import FastAPIMiddleware
patch_all()

import json
import boto3
import httpx
from fastapi import FastAPI, Query, Request, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from exceptions import register_handlers, InventoryNotFoundError, OutOfStockError, ProductNotFoundError
from logger import get_logger
from model import Inventory
from auth import verify_jwt_token
import service
from config import settings

logger = get_logger(__name__)
app = FastAPI(title="Inventory Service", version="1.0.0")
app.add_middleware(FastAPIMiddleware, recorder=xray_recorder)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
register_handlers(app)

router = APIRouter()

INVENTORY_RESULT_TOPIC_ARN = "arn:aws:sns:ap-southeast-1:726101441380:inventory-result_ecom"


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("--> %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("<-- %s %s %d", request.method, request.url.path, response.status_code)
    return response


@app.get("/", tags=["Health"])
def health():
    return {"service": "inventory-service", "status": "ok"}


@router.post("/inventory", status_code=201, summary="Add inventory")
def add_inventory(item: Inventory, username: str = Depends(verify_jwt_token)):
    return service.add_inventory(item)


@router.get("/inventory", summary="List all inventory")
def get_all_inventory(username: str = Depends(verify_jwt_token)):
    return service.get_all_inventory()


@router.get("/inventory/{product_id}", summary="Get stock level")
def get_inventory(product_id: str):
    return service.get_inventory(product_id)


@router.put("/inventory/{product_id}", summary="Set stock level")
def update_inventory(product_id: str, stock: int = Query(..., ge=0), username: str = Depends(verify_jwt_token)):
    return service.update_inventory(product_id, stock)


@router.post("/inventory/{product_id}/decrement", summary="Decrement stock (internal)")
def decrement_stock(product_id: str, quantity: int = Query(..., gt=0)):
    """Internal endpoint called by order-service to reduce stock when an order is placed."""
    return service.decrement_stock(product_id, quantity)

app.include_router(router, prefix="/v1")


# API Gateway entry point
api_handler = Mangum(app, lifespan="off")



_sns = None


def _get_sns():
    global _sns
    if _sns is None:
        _sns = boto3.client("sns", region_name=settings.AWS_REGION)
    return _sns


def _publish_inventory_result(order_id: str, product_id: str, quantity: int, amount: float, user_id: str, status: str, reason: str = "") -> None:
    """Publish InventoryReserved or InventoryFailed to SNS for payment-service to consume."""
    _get_sns().publish(
        TopicArn=INVENTORY_RESULT_TOPIC_ARN,
        Message=json.dumps({
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "amount": amount,
            "user_id": user_id,
            "status": status,     # "RESERVED" or "FAILED"
            "reason": reason,
        }),
    )
    logger.info("Inventory result published: order_id=%s status=%s", order_id, status)
    try:
        httpx.post("http://localhost:8005/v1/analytics/publish-event", json={
            "event_type": "order_status_update",
            "data": {
                "order_id": order_id,
                "status": f"INVENTORY_{status}",
                "product_id": product_id,
                "quantity": quantity,
                "amount": float(amount),
                "user_id": user_id,
                "reason": reason
            }
        }, timeout=1.0)
    except Exception as e:
        logger.warning("Analytics WS broadcast failed: %s", e)


def _process_order_created(message: dict) -> None:
    """Handle a single OrderCreated event: decrement stock, then publish the result."""
    order_id = message["order_id"]
    product_id = message["product_id"]
    quantity = message["quantity"]
    amount = message.get("amount", 0)
    user_id = message.get("user_id", "")

    logger.info("SQS | Processing OrderCreated: order_id=%s product=%s qty=%d", order_id, product_id, quantity)

    try:
        service.decrement_stock(product_id, quantity)
        logger.info("SQS | Stock decremented for order_id=%s", order_id)
        _publish_inventory_result(order_id, product_id, quantity, amount, user_id, status="RESERVED")
    except (InventoryNotFoundError, OutOfStockError) as e:
        logger.error("SQS | Inventory failure for order_id=%s: %s", order_id, e)
        _publish_inventory_result(order_id, product_id, quantity, amount, user_id, status="FAILED", reason=str(e))
        # Call order-service to mark as FAILED
        try:
            httpx.put(f"{settings.ORDER_SERVICE_URL}/v1/orders/{order_id}/status", params={"status": "FAILED"}, timeout=5.0)
            logger.info("HTTP | Marked order status as FAILED for order_id=%s", order_id)
        except Exception as http_err:
            logger.error("HTTP | Failed to mark order status as FAILED: %s", http_err)
        # Do not re-raise here — this is a business failure, not a transient error.
        # Re-raising would cause SQS to retry endlessly for something that will never succeed.


def handler(event, context):
    """
    Unified Lambda entry point.
    - If triggered by SQS (event has 'Records'), process each OrderCreated message.
    - Otherwise, treat it as an API Gateway event and delegate to Mangum/FastAPI.
    """
    if "Records" in event:
        for record in event["Records"]:
            sns_envelope = json.loads(record["body"])
            message = json.loads(sns_envelope["Message"])
            try:
                _process_order_created(message)
            except Exception as e:
                logger.error("SQS | Unexpected failure processing record: %s", e)
                raise  # transient/unexpected errors still trigger SQS retry -> DLQ
        return {"status": "processed"}

    # Not an SQS event -> API Gateway request
    return api_handler(event, context)