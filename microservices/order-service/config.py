from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str = "ap-southeast-1"
    TABLE_NAME: str = "orders_ecom"
    AWS_PROFILE: str = "idp-sbx-trn-lab-01"

    INVENTORY_SERVICE_URL: str = "https://g9c3k1vwe7.execute-api.ap-southeast-1.amazonaws.com"
    PAYMENT_SERVICE_URL: str = "https://f9ltky86oc.execute-api.ap-southeast-1.amazonaws.com"
    PRODUCT_SERVICE_URL: str = "https://izalnbyq9f.execute-api.ap-southeast-1.amazonaws.com"
    CART_SERVICE_URL: str = "https://55akltsjy7.execute-api.ap-southeast-1.amazonaws.com"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
