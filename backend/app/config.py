from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str
    FRONTEND_URL: str
    CLERK_SECRET_KEY: str
    DATABASE_URL: str


settings = Settings.model_validate({})
