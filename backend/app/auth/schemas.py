import uuid
from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints
from sqlmodel import Field, SQLModel

from app.schemas import AccountEmail

EmailCodePurpose = Literal["email_login", "password_reset"]

AuthPurpose = Literal["email_login", "password_login", "password_reset"]

EmailCode = Annotated[str, StringConstraints(pattern=r"^[0-9]{6}$")]

Password = Annotated[str, StringConstraints(min_length=8, max_length=128)]


class EmailRequest(SQLModel):
    """邮箱请求。"""

    model_config = {"extra": "forbid"}

    email: AccountEmail = Field(max_length=254, description="邮箱")


class EmailCodeSendRequest(EmailRequest):
    """验证码发送请求。"""

    purpose: EmailCodePurpose = Field(default="email_login", description="验证码用途")


class EmailCodeLoginRequest(EmailRequest):
    """验证码登录请求。"""

    code: EmailCode = Field(description="邮箱验证码")


class PasswordLoginRequest(EmailRequest):
    """密码登录请求。"""

    password: Password = Field(description="密码")


class PasswordResetRequest(EmailRequest):
    """密码重置请求。"""

    code: EmailCode = Field(description="邮箱验证码")
    password: Password = Field(description="密码")


class PasswordUpdateRequest(SQLModel):
    """密码设置或修改请求。"""

    model_config = {"extra": "forbid"}

    code: EmailCode = Field(description="邮箱验证码")
    password: Password = Field(description="密码")


class AuthSession(BaseModel):
    """会话数据，记录认证时的用户版本。"""

    user_id: uuid.UUID
    auth_version: int
