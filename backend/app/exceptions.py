"""Custom application exceptions and FastAPI exception handlers."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class InvalidObjectIdError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class InventoryNotFoundError(Exception):
    pass


class OutOfStockError(Exception):
    pass


class EmptyCartError(Exception):
    pass


class PaymentFailureError(Exception):
    pass


class OrderNotFoundError(Exception):
    pass


def register_exception_handlers(app: FastAPI) -> None:
    """Attach all custom exception handlers to the FastAPI app."""

    @app.exception_handler(InvalidObjectIdError)
    async def invalid_object_id(_: Request, exc: InvalidObjectIdError):
        return JSONResponse(status_code=400, content={"detail": "Invalid ID format"})

    @app.exception_handler(ProductNotFoundError)
    async def product_not_found(_: Request, exc: ProductNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Product Not Found"})

    @app.exception_handler(InventoryNotFoundError)
    async def inventory_not_found(_: Request, exc: InventoryNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Inventory Not Found"})

    @app.exception_handler(OutOfStockError)
    async def out_of_stock(_: Request, exc: OutOfStockError):
        return JSONResponse(status_code=400, content={"detail": "Out Of Stock"})

    @app.exception_handler(EmptyCartError)
    async def empty_cart(_: Request, exc: EmptyCartError):
        return JSONResponse(status_code=400, content={"detail": "Cart Is Empty"})

    @app.exception_handler(PaymentFailureError)
    async def payment_failure(_: Request, exc: PaymentFailureError):
        return JSONResponse(status_code=402, content={"detail": "Payment Failed"})

    @app.exception_handler(OrderNotFoundError)
    async def order_not_found(_: Request, exc: OrderNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Order Not Found"})
