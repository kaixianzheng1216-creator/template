from typing import Literal

from pydantic import BaseModel
from pydantic import Field as PydanticField
from sqlmodel import Field, SQLModel


class PaginationRequest(SQLModel):
    """分页与排序参数。"""

    model_config = {"extra": "forbid"}

    skip: int = Field(default=0, ge=0, le=2**63 - 1, description="跳过记录数")
    limit: int = Field(default=100, ge=1, le=100, description="最多返回记录数")
    order: Literal["asc", "desc"] = Field(default="desc", description="排序方向")


class PaginationResponse[ResponseDataT](BaseModel):
    """分页响应。"""

    data: list[ResponseDataT] = PydanticField(description="当前页数据")
    count: int = PydanticField(description="记录总数")
