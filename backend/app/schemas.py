from typing import Annotated

from pydantic import AfterValidator, BaseModel, EmailStr, Field

AccountEmail = Annotated[EmailStr, AfterValidator(str.casefold)]


class ValidationErrorDetail(BaseModel):
    """参数校验错误详情。"""

    field: str = Field(description="错误字段路径")
    type: str = Field(description="校验错误类型")


class ErrorResponse(BaseModel):
    """统一错误响应。"""

    code: str = Field(description="错误代码")
    message: str = Field(description="错误提示")
    details: list[ValidationErrorDetail] | None = Field(
        default=None, description="参数校验错误详情"
    )
