import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

from app.schemas import PaginationResponse


class ItemCreate(SQLModel):
    """创建条目的请求数据。"""

    title: str = Field(
        min_length=1,
        max_length=255,
        description="条目标题",
    )
    description: str | None = Field(
        default=None,
        max_length=255,
        description="条目描述",
    )


class ItemUpdate(SQLModel):
    """更新条目的请求数据。"""

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="条目标题",
    )
    description: str | None = Field(
        default=None,
        max_length=255,
        description="条目描述",
    )


class ItemPublic(SQLModel):
    """条目的公开响应数据。"""

    id: uuid.UUID = Field(description="条目 ID")

    title: str = Field(description="条目标题")
    description: str | None = Field(default=None, description="条目描述")

    owner_id: uuid.UUID = Field(description="所属用户 ID")

    created_at: datetime | None = Field(default=None, description="创建时间")


class ItemsPublic(PaginationResponse[ItemPublic]):
    """条目列表的响应数据。"""
