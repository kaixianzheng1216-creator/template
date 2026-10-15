import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

from app.schemas import PaginationResponse


class UserRegister(SQLModel):
    """用户注册的请求数据。"""

    username: str = Field(
        min_length=3,
        max_length=50,
        description="用户名",
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="登录密码",
    )
    full_name: str | None = Field(
        default=None,
        max_length=255,
        description="用户全名",
    )


class UserUpdateMe(SQLModel):
    """当前用户更新个人信息的请求数据。"""

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="用户名",
    )
    full_name: str | None = Field(
        default=None,
        max_length=255,
        description="用户全名",
    )


class UpdatePassword(SQLModel):
    """更新当前用户密码的请求数据。"""

    current_password: str = Field(
        min_length=8,
        max_length=128,
        description="当前密码",
    )
    new_password: str = Field(
        min_length=8,
        max_length=128,
        description="新密码",
    )


class UserCreate(SQLModel):
    """创建用户的请求数据。"""

    username: str = Field(
        min_length=3,
        max_length=50,
        description="用户名",
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="登录密码",
    )
    full_name: str | None = Field(
        default=None,
        max_length=255,
        description="用户全名",
    )
    is_active: bool = Field(default=True, description="是否启用")
    is_superuser: bool = Field(default=False, description="是否为超级用户")


class UserUpdate(SQLModel):
    """更新用户的请求数据。"""

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="用户名",
    )
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128,
        description="登录密码",
    )
    full_name: str | None = Field(
        default=None,
        max_length=255,
        description="用户全名",
    )
    is_active: bool | None = Field(default=None, description="是否启用")
    is_superuser: bool | None = Field(
        default=None,
        description="是否为超级用户",
    )


class UserPublic(SQLModel):
    """用户的公开响应数据。"""

    id: uuid.UUID = Field(description="用户 ID")
    username: str = Field(description="用户名")
    full_name: str | None = Field(default=None, description="用户全名")
    is_active: bool = Field(default=True, description="是否启用")
    is_superuser: bool = Field(default=False, description="是否为超级用户")
    created_at: datetime | None = Field(default=None, description="创建时间")


class UsersPublic(PaginationResponse[UserPublic]):
    """用户列表的响应数据。"""


class PrivateUserCreate(SQLModel):
    """创建开发测试用户的请求数据。"""

    username: str = Field(description="用户名")
    password: str = Field(description="登录密码")
    full_name: str = Field(description="用户全名")
