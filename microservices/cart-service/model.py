from pydantic import BaseModel


class Cart(BaseModel):
    user_id: str
    product_id: str
    quantity: int

    model_config = {"json_schema_extra": {"examples": [{"user_id": "user1", "product_id": "abc-123", "quantity": 2}]}}
