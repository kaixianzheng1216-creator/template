from collections.abc import Mapping
from typing import ClassVar

from fastapi import status
from starlette.exceptions import HTTPException


class AppError(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: ClassVar[str] = "INTERNAL_SERVER_ERROR"
    detail: str = "服务器内部错误"

    def __init__(self, *, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=headers
        )
