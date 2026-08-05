from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from exceptions import register_handlers
from logger import get_logger
from model import RegisterRequest, VerifyRequest, LoginRequest, OrderEmailRequest
import service
from auth import verify_jwt_token

logger = get_logger(__name__)
app = FastAPI(title="Auth Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
register_handlers(app)

router = APIRouter()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("--> %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("<-- %s %s %d", request.method, request.url.path, response.status_code)
    return response

@app.get("/", tags=["Health"])
def health():
    return {"service": "auth-service", "status": "ok"}

@router.post("/auth/register", status_code=201, summary="Register a new account")
def register(req: RegisterRequest):
    if req.password != req.confirm_password:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Passwords do not match")
    return service.register_user(req.name, req.email, req.password)

@router.post("/auth/verify", summary="Verify email registration code")
def verify(req: VerifyRequest):
    return service.verify_code(req.email, req.verification_code)

@router.post("/auth/login", summary="Login user")
def login(req: LoginRequest):
    return service.login_user(req.email, req.password)

@router.get("/auth/users", summary="List all registered users (admin-only)")
def get_users(username: str = Depends(verify_jwt_token)):
    from config import settings
    from fastapi import HTTPException
    if username != settings.ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Forbidden: Only admin can view users")
    return service.get_all_users()

@router.post("/auth/send-order-email", summary="Send order confirmation email via SES")
def send_order_email(req: OrderEmailRequest, username: str = Depends(verify_jwt_token)):
    return service.send_order_confirmation(req)

app.include_router(router, prefix="/v1")

handler = Mangum(app)
