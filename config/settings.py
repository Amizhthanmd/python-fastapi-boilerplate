from pydantic_settings import BaseSettings

#TODO Change in production
class Settings(BaseSettings):
    SECRET_KEY: str = "ARS@123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 168  #7 days

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
