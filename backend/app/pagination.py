from typing import Literal

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class ListQuery(SQLModel):
    """列表分页与排序参数。"""

    skip: int = Field(default=0, ge=0, le=2**63 - 1, description="跳过的记录数量")
    limit: int = Field(
        default=100,
        ge=1,
        le=100,
        description="返回的最大记录数量",
    )
    order: Literal["asc", "desc"] = Field(default="desc", description="排序方向")


class PaginationResponse[ResponseDataT](BaseModel):
    """分页查询响应。"""

    data: list[ResponseDataT] = Field(description="当前页数据")
    count: int = Field(description="记录总数")
