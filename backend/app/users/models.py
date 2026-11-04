import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=254)
    password_hash: str | None = Field(default=None, max_length=255)
    name: str = Field(max_length=255)
    avatar_url: str = Field(
        default_factory=lambda: (
            f"https://api.dicebear.com/10.x/notionists/svg?seed={uuid.uuid4()}"
            "&backgroundColor=ffffff"
        ),
        max_length=2048,
    )
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)
    auth_version: int = Field(default=0)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), sa_type=DateTime(timezone=True)
    )

    @property
    def has_password(self) -> bool:
        return self.password_hash is not None
