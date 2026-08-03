from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class OrderNotFoundError(Exception):
    pass


class InventoryNotFoundError(Exception):
    pass


class OutOfStockError(Exception):
    pass


def register_handlers(app: FastAPI) -> None:
    @app.exception_handler(OrderNotFoundError)
    async def _(_: Request, __: OrderNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Order Not Found"})

    @app.exception_handler(InventoryNotFoundError)
    async def _(_: Request, __: InventoryNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Inventory Not Found"})

    @app.exception_handler(OutOfStockError)
    async def _(_: Request, __: OutOfStockError):
        return JSONResponse(status_code=400, content={"detail": "Out Of Stock"})
