from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class CartItemNotFoundError(Exception):
    pass


def register_handlers(app: FastAPI) -> None:
    @app.exception_handler(CartItemNotFoundError)
    async def _(_: Request, __: CartItemNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Cart Item Not Found"})
