import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


class Content(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    owner_id: str = Field(max_length=255, index=True, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )
