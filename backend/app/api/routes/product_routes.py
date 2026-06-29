"""Product endpoints."""

from fastapi import APIRouter, Depends
from pymongo.collection import Collection

from app.dependencies import products_col
from app.logger import get_logger
from app.models.product import Product
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])
logger = get_logger(__name__)


@router.post(
    "",
    status_code=201,
    summary="Create a product",
    description="Add a new product to the catalogue.",
    responses={201: {"description": "Product created"}, 422: {"description": "Validation error"}},
)
def create_product(product: Product, col: Collection = Depends(products_col)):
    logger.info("POST /products | name=%s", product.name)
    return product_service.create_product(product, col)


@router.get(
    "",
    summary="List all products",
    description="Retrieve every product in the catalogue.",
)
def get_products(col: Collection = Depends(products_col)):
    logger.info("GET /products")
    return product_service.get_products(col)


@router.get(
    "/{product_id}",
    summary="Get a product",
    description="Retrieve a single product by its MongoDB ObjectId.",
    responses={400: {"description": "Invalid ID"}, 404: {"description": "Product not found"}},
)
def get_product(product_id: str, col: Collection = Depends(products_col)):
    logger.info("GET /products/%s", product_id)
    return product_service.get_product(product_id, col)


@router.put(
    "/{product_id}",
    summary="Update a product",
    description="Replace all fields of an existing product.",
    responses={400: {"description": "Invalid ID"}, 404: {"description": "Product not found"}},
)
def update_product(product_id: str, product: Product, col: Collection = Depends(products_col)):
    logger.info("PUT /products/%s", product_id)
    return product_service.update_product(product_id, product, col)


@router.delete(
    "/{product_id}",
    summary="Delete a product",
    description="Permanently remove a product from the catalogue.",
    responses={400: {"description": "Invalid ID"}, 404: {"description": "Product not found"}},
)
def delete_product(product_id: str, col: Collection = Depends(products_col)):
    logger.info("DELETE /products/%s", product_id)
    return product_service.delete_product(product_id, col)
