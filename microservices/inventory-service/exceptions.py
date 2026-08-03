from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class InventoryNotFoundError(Exception):
    pass


class OutOfStockError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


def register_handlers(app: FastAPI) -> None:
    @app.exception_handler(InventoryNotFoundError)
    async def _(_: Request, __: InventoryNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Inventory Not Found"})

    @app.exception_handler(OutOfStockError)
    async def __(_: Request, ___: OutOfStockError):
        return JSONResponse(status_code=400, content={"detail": "Out Of Stock"})

    @app.exception_handler(ProductNotFoundError)
    async def ___(__: Request, ____: ProductNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Product Not Found"})
