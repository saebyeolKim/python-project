from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    JWT_SECRET_KEY: str
    EMAIL_PASSWORD: str
    CELERY_BROKER_URL: str
    CELERY_BACKEND_URL: str

@lru_cache
def get_settings():
    return Settings()