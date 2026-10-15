import uuid
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def get_datetime_utc() -> datetime:
    current_time = datetime.now(UTC)

    return current_time


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True, index=True, min_length=3, max_length=50)
    hashed_password: str
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime | None = Field(default_factory=get_datetime_utc)
