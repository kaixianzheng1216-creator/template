from typing import ClassVar

from fastapi import status


class AppException(Exception):
    """所有可安全返回给客户端的业务异常基类。"""

    status_code: ClassVar[int] = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: ClassVar[str] = "INTERNAL_SERVER_ERROR"
    message: ClassVar[str] = "服务器内部错误"

    def __init__(self) -> None:
        super().__init__(self.message)
