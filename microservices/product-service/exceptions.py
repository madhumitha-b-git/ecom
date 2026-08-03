from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ProductNotFoundError(Exception):
    pass


class InvalidProductIdError(Exception):
    pass


def register_handlers(app: FastAPI) -> None:
    @app.exception_handler(ProductNotFoundError)
    async def _(_: Request, __: ProductNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Product Not Found"})

    @app.exception_handler(InvalidProductIdError)
    async def __(_: Request, ___: InvalidProductIdError):
        return JSONResponse(status_code=400, content={"detail": "Invalid product_id"})
