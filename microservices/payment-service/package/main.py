import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from exceptions import register_handlers
from logger import get_logger
from model import Payment
import service

logger = get_logger(__name__)
app = FastAPI(title="Payment Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
register_handlers(app)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("→ %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("← %s %s %d", request.method, request.url.path, response.status_code)
    return response


@app.get("/", tags=["Health"])
def health():
    return {"service": "payment-service", "status": "ok"}


@app.post("/payments", status_code=201, summary="Process payment")
def create_payment(payment: Payment):
    return service.create_payment(payment)


@app.get("/payments", summary="List all payments")
def get_payments():
    return service.get_payments()


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
    service.create_payment(payment)
    logger.info("SQS | Payment processed for order_id=%s", order_id)


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