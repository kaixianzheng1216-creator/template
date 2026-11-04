from typing import Annotated

from pydantic import AfterValidator, BaseModel, EmailStr

AccountEmail = Annotated[EmailStr, AfterValidator(str.casefold)]


class ValidationErrorDetail(BaseModel):
    """参数校验错误详情。"""

    field: str
    type: str


class ErrorResponse(BaseModel):
    """统一错误响应。"""

    code: str
    message: str
    details: list[ValidationErrorDetail] | None = None
