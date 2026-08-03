from pydantic import BaseModel


class Payment(BaseModel):
    order_id: str
    amount: float
    method: str = "CARD"

    model_config = {"json_schema_extra": {"examples": [{"order_id": "ord-123", "amount": 179.98, "method": "upi"}]}}
