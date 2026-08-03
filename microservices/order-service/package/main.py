from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from exceptions import register_handlers
from logger import get_logger
from model import Order
import service

logger = get_logger(__name__)
app = FastAPI(title="Order Service", version="1.0.0")
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
    return {"service": "order-service", "status": "ok"}


@app.post("/orders", status_code=201, summary="Place an order")
def create_order(order: Order):
    return service.create_order(order)


@app.get("/orders", summary="List all orders")
def get_orders():
    return service.get_orders()


@app.get("/orders/{order_id}", summary="Get order by ID")
def get_order(order_id: str):
    return service.get_order(order_id)


# Lambda entry point
handler = Mangum(app)
