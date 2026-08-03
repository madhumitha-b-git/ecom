from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_REGION: str = "ap-southeast-1"
    AWS_PROFILE: str = "idp-sbx-trn-lab-01"
    S3_RAW_BUCKET: str = ""
    S3_STAGE_BUCKET: str = ""
    
    ORDER_SERVICE_URL: str = "http://localhost:8000"
    CART_SERVICE_URL: str = "http://localhost:8001"
    INVENTORY_SERVICE_URL: str = "http://localhost:8002"
    PAYMENT_SERVICE_URL: str = "http://localhost:8003"
    PRODUCT_SERVICE_URL: str = "http://localhost:8004"

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
