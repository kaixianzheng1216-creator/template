import uuid
from datetime import datetime
from typing import Annotated, Literal

from pydantic import StringConstraints
from sqlmodel import Field, SQLModel

from app.pagination import PaginationRequest, PaginationResponse

UserName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
]


class UserProfileUpdateRequest(SQLModel):
    """用户资料更新请求。"""

    model_config = {"extra": "forbid"}

    name: UserName = Field(description="昵称")


class UserListRequest(PaginationRequest):
    """用户查询参数。"""

    search: str = Field(default="", max_length=255, description="按邮箱或昵称搜索")
    is_active: bool | None = Field(default=None, description="是否启用")
    sort: Literal["name", "created_at"] = Field(
        default="created_at", description="排序字段"
    )


class UserRoleUpdateRequest(SQLModel):
    """用户角色更新请求。"""

    model_config = {"extra": "forbid"}

    is_admin: bool = Field(description="是否为管理员")


class UserStatusUpdateRequest(SQLModel):
    """用户状态更新请求。"""

    model_config = {"extra": "forbid"}

    is_active: bool = Field(description="是否启用")


class UserBatchDeleteRequest(SQLModel):
    """用户批量删除请求。"""

    model_config = {"extra": "forbid"}

    ids: list[uuid.UUID] = Field(
        min_length=1, max_length=100, description="待删除用户 ID"
    )


class UserResponse(SQLModel):
    """用户响应。"""

    id: uuid.UUID = Field(description="用户 ID")
    email: str = Field(description="邮箱")
    has_password: bool = Field(description="是否已设置密码")
    name: str = Field(description="昵称")
    avatar_url: str = Field(description="头像地址")
    is_admin: bool = Field(description="是否为管理员")
    is_active: bool = Field(description="是否启用")
    created_at: datetime = Field(description="创建时间")


class UserListResponse(PaginationResponse[UserResponse]):
    """用户列表响应。"""
