from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from exceptions import register_handlers
from logger import get_logger
from model import Product
from auth import verify_jwt_token, verify_admin_token
import service

logger = get_logger(__name__)
app = FastAPI(title="Product Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
register_handlers(app)

router = APIRouter()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("→ %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("← %s %s %d", request.method, request.url.path, response.status_code)
    return response


@app.get("/", tags=["Health"])
def health():
    return {"service": "product-service", "status": "ok"}


@router.post("/products", status_code=201, summary="Create product")
def create_product(product: Product, username: str = Depends(verify_jwt_token)):
    return service.create_product(product)


@router.get("/products", summary="List all products")
def get_products():
    return service.get_products()


@router.get("/products/{product_id}", summary="Get product by ID")
def get_product(product_id: str):
    return service.get_product(product_id)


@router.put("/products/{product_id}", summary="Update product")
def update_product(product_id: str, product: Product, username: str = Depends(verify_jwt_token)):
    return service.update_product(product_id, product)


@router.delete("/products/{product_id}", summary="Delete product")
def delete_product(product_id: str, username: str = Depends(verify_jwt_token)):
    return service.delete_product(product_id)


from pydantic import BaseModel
import auth_service

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str

class VerifyRequest(BaseModel):
    email: str
    verification_code: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/register", status_code=201, summary="Register a new account")
def register(req: RegisterRequest):
    if req.password != req.confirm_password:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Passwords do not match")
    return auth_service.register_user(req.name, req.email, req.password)

@router.post("/auth/verify", summary="Verify email registration code")
def verify(req: VerifyRequest):
    return auth_service.verify_code(req.email, req.verification_code)

@router.post("/auth/login", summary="Login user")
def login(req: LoginRequest):
    return auth_service.login_user(req.email, req.password)

@router.get("/auth/users", summary="List all registered users (admin-only)")
def get_users(username: str = Depends(verify_admin_token)):
    return auth_service.get_all_users()


app.include_router(router, prefix="/v1")


# Lambda entry point
handler = Mangum(app, lifespan="off")

