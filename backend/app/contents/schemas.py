import uuid
from datetime import datetime
from typing import Annotated, Literal

from pydantic import StringConstraints
from sqlmodel import Field, SQLModel

from app.pagination import ListQuery, PaginationResponse

ContentTitle = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
]


class ContentListQuery(ListQuery):
    title: str = Field(default="", max_length=255, description="标题包含")
    description: str = Field(default="", max_length=255, description="说明包含")
    sort: Literal["title", "created_at"] = "created_at"
    created_after: datetime | None = Field(default=None, description="创建时间起点")


class ContentCreate(SQLModel):
    """创建内容的请求数据。"""

    title: ContentTitle = Field(
        description="内容标题",
    )
    description: str | None = Field(
        default=None,
        max_length=255,
        description="内容描述",
    )


class ContentUpdate(SQLModel):
    """更新内容的请求数据。"""

    title: ContentTitle = Field(description="内容标题")
    description: str | None = Field(
        max_length=255,
        description="内容描述",
    )


class ContentBatchDelete(SQLModel):
    ids: list[uuid.UUID] = Field(
        min_length=1, max_length=100, description="待删除的内容 ID"
    )


class ContentPublic(SQLModel):
    """内容的公开响应数据。"""

    id: uuid.UUID = Field(description="内容 ID")
    title: str = Field(description="内容标题")
    description: str | None = Field(description="内容描述")
    owner_id: str = Field(description="Clerk 用户 ID")
    created_at: datetime = Field(description="创建时间")


class ContentsPublic(PaginationResponse[ContentPublic]):
    """内容列表的响应数据。"""
