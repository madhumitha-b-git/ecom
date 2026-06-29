"""Inventory endpoints."""

from fastapi import APIRouter, Depends, Query
from pymongo.collection import Collection

from app.dependencies import inventory_col
from app.logger import get_logger
from app.models.inventory import Inventory
from app.services import inventory_service

router = APIRouter(prefix="/inventory", tags=["Inventory"])
logger = get_logger(__name__)


@router.post(
    "",
    status_code=201,
    summary="Add inventory",
    description="Create an inventory record for a product.",
    responses={201: {"description": "Inventory added"}, 422: {"description": "Validation error"}},
)
def add_inventory(item: Inventory, col: Collection = Depends(inventory_col)):
    logger.info("POST /inventory | product_id=%s stock=%d", item.product_id, item.stock)
    return inventory_service.add_inventory(item, col)


@router.get(
    "/{product_id}",
    summary="Get inventory",
    description="Retrieve current stock level for a product.",
    responses={404: {"description": "Inventory not found"}},
)
def get_inventory(product_id: str, col: Collection = Depends(inventory_col)):
    logger.info("GET /inventory/%s", product_id)
    return inventory_service.get_inventory(product_id, col)


@router.put(
    "/{product_id}",
    summary="Update stock",
    description="Set the stock quantity for a product.",
    responses={404: {"description": "Inventory not found"}},
)
def update_inventory(
    product_id: str,
    stock: int = Query(..., ge=0, description="New stock level"),
    col: Collection = Depends(inventory_col),
):
    logger.info("PUT /inventory/%s | stock=%d", product_id, stock)
    return inventory_service.update_inventory(product_id, stock, col)
