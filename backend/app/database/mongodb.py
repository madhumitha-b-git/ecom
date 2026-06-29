"""Named collection accessors built on top of the single connection."""

from pymongo.collection import Collection

from app.database.connection import get_database


def get_products_collection() -> Collection:
    return get_database()["products"]


def get_inventory_collection() -> Collection:
    return get_database()["inventory"]


def get_cart_collection() -> Collection:
    return get_database()["cart"]


def get_orders_collection() -> Collection:
    return get_database()["orders"]


def get_payments_collection() -> Collection:
    return get_database()["payments"]
