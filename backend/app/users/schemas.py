from datetime import datetime
from typing import Literal

from sqlmodel import Field, SQLModel

from app.pagination import ListQuery, PaginationResponse


class UserListQuery(ListQuery):
    full_name: str = Field(default="", max_length=255, description="姓名包含")
    email: str = Field(default="", max_length=255, description="邮箱包含")
    sort: Literal["name", "created_at"] = "created_at"
    banned: bool | None = Field(default=None, description="是否封禁")


class UserRoleUpdate(SQLModel):
    """更新 Clerk 用户角色。"""

    is_admin: bool = Field(description="是否为管理员")


class UserStatusUpdate(SQLModel):
    """更新 Clerk 用户封禁状态。"""

    banned: bool = Field(description="是否封禁")


class UserPublic(SQLModel):
    """来自 Clerk 的用户公开数据。"""

    id: str = Field(description="Clerk 用户 ID")
    email: str | None = Field(description="主邮箱")
    full_name: str | None = Field(description="姓名")
    banned: bool = Field(description="是否封禁")
    is_admin: bool = Field(description="是否为管理员")
    created_at: datetime = Field(description="创建时间")


class UsersPublic(PaginationResponse[UserPublic]):
    """用户列表的响应数据。"""
