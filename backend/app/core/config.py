import warnings
from typing import Literal, Self

from pydantic import (
    HttpUrl,
    PostgresDsn,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.exceptions import DefaultSecretError


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    FRONTEND_HOST: str = "http://localhost:3000"
    FASTAPI_ENV: Literal["development"] | None = None
    SENTRY_DSN: HttpUrl | None = None

    DATABASE_URL: PostgresDsn

    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    USERNAME_TEST_USER: str = "testuser"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def _use_psycopg_driver(cls, value: str | PostgresDsn) -> str:
        database_url = str(value)

        for scheme in ("postgres://", "postgresql://"):
            if database_url.startswith(scheme):
                database_url = database_url.replace(
                    scheme,
                    "postgresql+psycopg://",
                    1,
                )

                break

        return database_url

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)

        for host in self.DATABASE_URL.hosts():
            self._check_default_secret("DATABASE_URL password", host["password"])

        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            error = DefaultSecretError(var_name)

            if self.FASTAPI_ENV == "development":
                warnings.warn(str(error), stacklevel=1)
            else:
                raise error


settings = Settings()  # type: ignore # ty: ignore[unused-ignore-comment]
