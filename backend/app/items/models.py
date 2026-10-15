import uuid
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def get_datetime_utc() -> datetime:
    current_time = datetime.now(UTC)

    return current_time


class Item(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id",
        nullable=False,
        ondelete="CASCADE",
    )
    created_at: datetime | None = Field(default_factory=get_datetime_utc)
