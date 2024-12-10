import logging
import secrets
from functools import lru_cache
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", env_file_encoding="utf-8"
    )
    # APP
    RUN_ENV: str = "local"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = []
    PROJECT_NAME: str
    AUTHENTICATION_API_RATE_LIMIT: str = "5 per minute"
    SECURE_COOKIE: bool = True

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # RabbitMQ
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "root"
    RABBITMQ_PASSWORD: str = "rabbitmq-password"

    # Logging
    LOG_JSON_FORMAT: bool = False
    LOG_LEVEL: int = logging.INFO

    # Auth
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Mail
    SENDER_EMAIL: str = "test@test.com"
    SEND_WELCOME_EMAIL_MAX_RETRIES: int = 5
    SEND_WELCOME_EMAIL_RETRY_BACKOFF_VALUE: int = 5

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_uri(cls, field_value, info: ValidationInfo) -> str:
        if isinstance(field_value, str):
            return field_value
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=info.data.get("POSTGRES_DB") or "",
            port=info.data.get("POSTGRES_PORT"),
        ).unicode_string()

    @property
    def rabbitmq_url(self) -> str:
        """Construct the RabbitMQ URL for the broker."""
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}//"


settings = Settings()


@lru_cache()
def get_settings():
    return settings
