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
    model_config = {"extra": "forbid"}

    email: AccountEmail = Field(max_length=254, description="邮箱")


class EmailCodeSendRequest(EmailRequest):
    purpose: EmailCodePurpose = Field(default="email_login", description="验证码用途")


class EmailCodeSendResponse(SQLModel):
    has_password: bool = Field(description="是否已设置密码")


class EmailCodeLoginRequest(EmailRequest):
    code: EmailCode = Field(description="邮箱验证码")


class PasswordLoginRequest(EmailRequest):
    password: Password = Field(description="密码")


class PasswordResetRequest(EmailRequest):
    code: EmailCode = Field(description="邮箱验证码")
    password: Password = Field(description="密码")


class PasswordUpdateRequest(SQLModel):
    model_config = {"extra": "forbid"}

    code: EmailCode = Field(description="邮箱验证码")
    password: Password = Field(description="密码")


class AuthSession(BaseModel):
    user_id: uuid.UUID
    auth_version: int
