from pydantic import BaseModel
from typing import List, Optional

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

class OrderItem(BaseModel):
    name: str
    quantity: int
    amount: float
    size: Optional[str] = ""

class OrderEmailRequest(BaseModel):
    to: str
    order_id: str
    user_name: str
    shipping_name: str
    shipping_address: str
    phone: Optional[str] = ""
    payment_method: str
    order_date: str
    items: List[OrderItem]
    total_paid: float
