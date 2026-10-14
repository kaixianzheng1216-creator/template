from typing import ClassVar

from fastapi import status


class AppException(Exception):
    """所有可安全返回给客户端的业务异常基类。"""

    status_code: ClassVar[int] = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: ClassVar[str] = "INTERNAL_SERVER_ERROR"
    message: ClassVar[str] = "服务器内部错误"

    def __init__(self) -> None:
        super().__init__(self.message)


class RequestValidationAppException(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    code = "REQUEST_VALIDATION_ERROR"
    message = "请求参数验证失败"


class HttpRequestException(AppException):
    code = "HTTP_REQUEST_ERROR"
    message = "请求处理失败"


class InternalServerException(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "INTERNAL_SERVER_ERROR"
    message = "服务器内部错误"
