from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from exceptions import register_handlers
from logger import get_logger
from model import Product
import service

logger = get_logger(__name__)
app = FastAPI(title="Product Service", version="1.0.0")
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
    return {"service": "product-service", "status": "ok"}


@app.post("/products", status_code=201, summary="Create product")
def create_product(product: Product):
    return service.create_product(product)


@app.get("/products", summary="List all products")
def get_products():
    return service.get_products()


@app.get("/products/{product_id}", summary="Get product by ID")
def get_product(product_id: str):
    return service.get_product(product_id)


@app.put("/products/{product_id}", summary="Update product")
def update_product(product_id: str, product: Product):
    return service.update_product(product_id, product)


@app.delete("/products/{product_id}", summary="Delete product")
def delete_product(product_id: str):
    return service.delete_product(product_id)


# Lambda entry point
handler = Mangum(app, lifespan="off", api_gateway_base_path="/proddev")
