from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from exceptions import register_handlers
from logger import get_logger
from model import Order
from auth import verify_jwt_token
import service

logger = get_logger(__name__)
app = FastAPI(title="Order Service", version="1.0.0")
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
    return {"service": "order-service", "status": "ok"}


@router.post("/orders", status_code=201, summary="Place an order")
def create_order(order: Order, username: str = Depends(verify_jwt_token)):
    return service.create_order(order)


@router.get("/orders", summary="List all orders")
def get_orders(username: str = Depends(verify_jwt_token)):
    is_admin = (
        username in ("admin", "admin@gmail.com", "madhumithamalu6@gmail.com", "mock_admin")
        or "admin" in username.lower()
    )
    if is_admin:
        return service.get_orders()
    else:
        return service.get_orders_for_user(username)


@router.get("/orders/{order_id}", summary="Get order by ID")
def get_order(order_id: str, username: str = Depends(verify_jwt_token)):
    return service.get_order(order_id)


@router.put("/orders/{order_id}/status", summary="Update order status (internal)")
def update_order_status(order_id: str, status: str):
    """Internal endpoint called by inventory-service or payment-service to update order status."""
    return service.update_order_status(order_id, status)

app.include_router(router, prefix="/v1")


# Lambda entry point
handler = Mangum(app)

