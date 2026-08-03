from pydantic import BaseModel


class Order(BaseModel):
    user_id: str
    product_id: str
    quantity: int
    amount: float
    size: str = ""
    shipping_name: str = ""
    shipping_address: str = ""
    phone: str = ""
    payment_method: str = ""

    model_config = {
        "json_schema_extra": {
            "examples": [{"user_id": "user1", "product_id": "abc-123", "quantity": 2, "amount": 179.98, "size": "M", "shipping_name": "Jane Doe", "shipping_address": "123 Main St", "phone": "9876543210", "payment_method": "upi"}]
        }
    }
