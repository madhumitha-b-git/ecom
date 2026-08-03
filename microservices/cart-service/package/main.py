from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from exceptions import register_handlers
from logger import get_logger
from model import Cart
import service

logger = get_logger(__name__)
app = FastAPI(title="Cart Service", version="1.0.0")
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
    return {"service": "cart-service", "status": "ok"}


@app.post("/cart", status_code=201, summary="Add item to cart")
def add_to_cart(item: Cart):
    return service.add_to_cart(item)


@app.get("/cart/{user_id}", summary="Get user cart")
def get_cart(user_id: str):
    return service.get_cart(user_id)


@app.delete("/cart/{cart_id}", summary="Remove cart item")
def delete_cart_item(cart_id: str):
    return service.delete_cart_item(cart_id)


# Lambda entry point
handler = Mangum(app, lifespan="off", api_gateway_base_path="/proddev")
