from sqlmodel import Field, SQLModel


class Token(SQLModel):
    """登录成功后的访问令牌响应。"""

    access_token: str = Field(description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")


class TokenPayload(SQLModel):
    """访问令牌中携带的数据。"""

    sub: str | None = Field(default=None, description="令牌主体的用户 ID")
