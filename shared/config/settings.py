from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings shared across services."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "microservice_ecosystem_core"
    environment: str = "development"
    database_url: str = Field(
        default="postgresql+psycopg2://ecosystem_user:ecosystem_password@localhost:5432/ecosystem_db",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    jwt_secret_key: str = Field(default="super-secret-key", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS")
    auth_service_url: str = Field(default="http://localhost:8001", alias="AUTH_SERVICE_URL")
    authorization_service_url: str = Field(default="http://localhost:8002", alias="AUTHORIZATION_SERVICE_URL")
    user_service_url: str = Field(default="http://localhost:8003", alias="USER_SERVICE_URL")
    service_registry_url: str = Field(default="http://localhost:8004", alias="SERVICE_REGISTRY_URL")
    demo_service_url: str = Field(default="http://localhost:8005", alias="DEMO_SERVICE_URL")
    rate_limit_requests: int = Field(default=60, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window_seconds: int = Field(default=60, alias="RATE_LIMIT_WINDOW_SECONDS")


@lru_cache
def get_settings() -> Settings:
    return Settings()
