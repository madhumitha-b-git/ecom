from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_REGION: str = "ap-southeast-1"
    TABLE_NAME: str = "payment_ecom"
    AWS_PROFILE: str = "idp-sbx-trn-lab-01"
    ORDER_SERVICE_URL: str = "https://uuz930mrx2.execute-api.ap-southeast-1.amazonaws.com"
    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()