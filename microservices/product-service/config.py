from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str = "ap-southeast-1"
    TABLE_NAME: str = "Products_ecom"
    AWS_PROFILE: str = "idp-sbx-trn-lab-01"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
