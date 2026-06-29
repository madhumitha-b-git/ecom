"""FastAPI dependency callables for injecting collections."""

from fastapi import Depends
from pymongo.collection import Collection

from app.database.mongodb import (
    get_cart_collection,
    get_inventory_collection,
    get_orders_collection,
    get_payments_collection,
    get_products_collection,
)


def products_col() -> Collection:
    return get_products_collection()


def inventory_col() -> Collection:
    return get_inventory_collection()


def cart_col() -> Collection:
    return get_cart_collection()


def orders_col() -> Collection:
    return get_orders_collection()


def payments_col() -> Collection:
    return get_payments_collection()
