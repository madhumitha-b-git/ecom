from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class OrderNotFoundError(Exception):
    pass


class InventoryNotFoundError(Exception):
    pass


class OutOfStockError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class CartClearError(Exception):
    pass


def register_handlers(app: FastAPI) -> None:
    @app.exception_handler(OrderNotFoundError)
    async def _(_: Request, __: OrderNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Order Not Found"})

    @app.exception_handler(InventoryNotFoundError)
    async def __(_: Request, ___: InventoryNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Inventory Not Found"})

    @app.exception_handler(OutOfStockError)
    async def ___(_: Request, ____: OutOfStockError):
        return JSONResponse(status_code=400, content={"detail": "Out Of Stock"})

    @app.exception_handler(ProductNotFoundError)
    async def ____(_: Request, _____: ProductNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Product Not Found"})

    @app.exception_handler(CartClearError)
    async def _____(_: Request, ______: CartClearError):
        return JSONResponse(status_code=500, content={"detail": "Failed to clear cart"})
