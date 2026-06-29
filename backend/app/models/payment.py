from pydantic import BaseModel


class Payment(BaseModel):
    order_id: str
    amount: float

    model_config = {
        "json_schema_extra": {
            "examples": [{"order_id": "64abc456", "amount": 179.98}]
        }
    }
