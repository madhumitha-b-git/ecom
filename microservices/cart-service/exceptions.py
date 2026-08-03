from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class CartItemNotFoundError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


def register_handlers(app: FastAPI) -> None:
    @app.exception_handler(CartItemNotFoundError)
    async def _(_: Request, __: CartItemNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Cart Item Not Found"})

    @app.exception_handler(ProductNotFoundError)
    async def __(_: Request, ___: ProductNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Product Not Found"})
