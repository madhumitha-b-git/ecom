from pydantic import BaseModel


class Inventory(BaseModel):
    product_id: str
    stock: int

    model_config = {"json_schema_extra": {"examples": [{"product_id": "abc-123", "stock": 100}]}}
