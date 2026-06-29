"""FastAPI application factory and entry point."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import cart_routes, inventory_routes, order_routes, payment_routes, product_routes
from app.exceptions import register_exception_handlers
from app.logger import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="E-Commerce Backend",
        version="1.0.0",
        description="Production-ready FastAPI e-commerce backend with MongoDB.",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(product_routes.router)
    app.include_router(inventory_routes.router)
    app.include_router(cart_routes.router)
    app.include_router(payment_routes.router)
    app.include_router(order_routes.router)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info("→ %s %s", request.method, request.url.path)
        response = await call_next(request)
        logger.info("← %s %s %d", request.method, request.url.path, response.status_code)
        return response

    @app.get("/", tags=["Health"], summary="Health check")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
