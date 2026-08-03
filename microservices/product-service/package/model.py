from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    category: str
    price: float

    model_config = {
        "json_schema_extra": {
            "examples": [{"name": "Headphones", "description": "Wireless", "category": "Electronics", "price": 89.99}]
        }
    }
