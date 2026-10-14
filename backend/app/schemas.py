from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

ResponseDataT = TypeVar("ResponseDataT")


class PaginationRequest(SQLModel):
    """分页查询参数。"""

    skip: int = Field(default=0, description="跳过的记录数量")
    limit: int = Field(default=100, description="返回的最大记录数量")


class PaginationResponse(BaseModel, Generic[ResponseDataT]):  # noqa: UP046
    """分页查询响应。"""

    data: list[ResponseDataT] = Field(description="当前页数据")
    count: int = Field(description="记录总数")


class ErrorResponse(SQLModel):
    """统一错误响应。"""

    code: str = Field(description="错误码")
    message: str = Field(description="错误消息")


class ValidationErrorResponse(ErrorResponse):
    """请求参数验证错误响应。"""

    details: list[dict[str, Any]] = Field(description="字段验证错误列表")
