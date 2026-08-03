from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str = "ap-southeast-1"
    TABLE_NAME: str = "orders_ecom"
    AWS_PROFILE: str = "idp-sbx-trn-lab-01"

    # URLs of the other Lambda functions via API Gateway
    INVENTORY_SERVICE_URL: str = ""
    PAYMENT_SERVICE_URL: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
