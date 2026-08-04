from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.fastapi.middleware import FastAPIMiddleware
patch_all()

from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from exceptions import register_handlers
from logger import get_logger
from model import Cart
from auth import verify_jwt_token
import service

logger = get_logger(__name__)
app = FastAPI(title="Cart Service", version="1.0.0")
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
    return {"service": "cart-service", "status": "ok"}


@router.post("/cart", status_code=201, summary="Add item to cart")
def add_to_cart(item: Cart, username: str = Depends(verify_jwt_token)):
    return service.add_to_cart(item)


@router.get("/cart/{user_id}", summary="Get user cart")
def get_cart(user_id: str, username: str = Depends(verify_jwt_token)):
    return service.get_cart(user_id)


@router.delete("/cart/{cart_id}", summary="Remove cart item")
def delete_cart_item(cart_id: str, username: str = Depends(verify_jwt_token)):
    return service.delete_cart_item(cart_id)


@router.delete("/cart/user/{user_id}", summary="Clear all items for a user")
def clear_user_cart(user_id: str, username: str = Depends(verify_jwt_token)):
    return service.clear_user_cart(user_id)

app.include_router(router, prefix="/v1")


# Lambda entry point
handler = Mangum(app, lifespan="off")

