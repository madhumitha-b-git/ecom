from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_REGION: str = "ap-southeast-1"
    TABLE_NAME: str = "ecom-users"
    AWS_PROFILE: str = "idp-sbx-trn-lab-01"
    ADMIN_EMAIL: str = "madhumithamalu6@gmail.com"
    SMTP_PASSWORD: str = "" # We will configure this in .env
    SMTP_SENDER: str = "madhumithamalu6@gmail.com"

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
