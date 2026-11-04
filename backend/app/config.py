from pathlib import Path

from pydantic import EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.schemas import AccountEmail


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore",
    )

    PROJECT_NAME: str = Field(min_length=1)

    DATABASE_URL: str = Field(min_length=1)

    REDIS_URL: SecretStr = Field(min_length=1)

    ADMIN_EMAIL: AccountEmail = Field(max_length=254)
    ADMIN_PASSWORD: SecretStr = Field(min_length=8, max_length=128)

    DEV_LOGIN_ENABLED: bool = False

    SESSION_COOKIE_SECURE: bool = True
    SESSION_MAX_AGE_SECONDS: int = Field(default=604800, gt=0)

    EMAIL_CODE_SECRET: SecretStr = Field(min_length=32)
    RESEND_API_KEY: SecretStr = Field(min_length=1)
    EMAIL_FROM: EmailStr


settings = Settings.model_validate({})
