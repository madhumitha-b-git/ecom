from pydantic import BaseModel


class Order(BaseModel):
    user_id: str
    product_id: str
    quantity: int
    amount: float

    model_config = {
        "json_schema_extra": {
            "examples": [{"user_id": "user1", "product_id": "abc-123", "quantity": 2, "amount": 179.98}]
        }
    }
