import uuid
from datetime import datetime
from typing import Annotated, Literal

from pydantic import AwareDatetime, StringConstraints
from sqlmodel import Field, SQLModel

from app.pagination import PaginationRequest, PaginationResponse

ContentTitle = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
]


class ContentListRequest(PaginationRequest):
    search: str = Field(default="", max_length=255, description="按标题或描述搜索")
    created_after: AwareDatetime | None = Field(
        default=None, description="创建时间下限（含边界，必须带时区）"
    )
    sort: Literal["title", "created_at"] = Field(
        default="created_at", description="排序字段"
    )


class ContentCreateRequest(SQLModel):
    model_config = {"extra": "forbid"}

    title: ContentTitle = Field(description="内容标题")
    description: str | None = Field(
        default=None, max_length=255, description="内容描述"
    )


class ContentUpdateRequest(ContentCreateRequest):
    pass


class ContentBatchDeleteRequest(SQLModel):
    model_config = {"extra": "forbid"}

    ids: list[uuid.UUID] = Field(
        min_length=1, max_length=100, description="待删除内容 ID"
    )


class ContentResponse(SQLModel):
    id: uuid.UUID = Field(description="内容 ID")
    title: str = Field(description="内容标题")
    description: str | None = Field(description="内容描述")
    created_at: datetime = Field(description="创建时间")


class ContentListResponse(PaginationResponse[ContentResponse]):
    pass


class AdminContentListRequest(ContentListRequest):
    owner: str = Field(default="", max_length=255, description="按邮箱或昵称搜索")


class ContentOwnerResponse(SQLModel):
    id: uuid.UUID = Field(description="用户 ID")
    email: str = Field(description="邮箱")
    name: str = Field(description="昵称")
    avatar_url: str = Field(description="头像地址")


class AdminContentResponse(ContentResponse):
    owner: ContentOwnerResponse = Field(description="所属用户")


class AdminContentListResponse(PaginationResponse[AdminContentResponse]):
    pass
