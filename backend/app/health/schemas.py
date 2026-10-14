from pydantic import Field, RootModel


class HealthResponse(RootModel[bool]):
    """服务健康状态响应。"""

    root: bool = Field(description="服务是否健康")
