from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    PORT: int
    SALT: str
    SQLITE:  str
    ENV: str
    SECRET_KEY: str
    ALGORITHM: str   # ✅ add this
    ACCESS_TOKEN_EXPIRE_MINUTES: int  # ✅ add this
    ACCESS_TOKEN_EXPIRE_DAYS: int     # ✅ add this
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION:str
    AWS_BUCKET_NAME: str
        

    class Config:
        env_file = ".env"

settings = Settings()