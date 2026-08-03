from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class PaymentFailureError(Exception):
    pass


def register_handlers(app: FastAPI) -> None:
    @app.exception_handler(PaymentFailureError)
    async def _(_: Request, __: PaymentFailureError):
        return JSONResponse(status_code=402, content={"detail": "Payment Failed"})
