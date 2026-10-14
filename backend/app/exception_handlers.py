import logging
from typing import Any, cast

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions import (
    AppException,
    HttpRequestException,
    InternalServerException,
    RequestValidationAppException,
)

logger = logging.getLogger(__name__)

HTTP_ERROR_MESSAGES = {
    status.HTTP_400_BAD_REQUEST: "请求错误",
    status.HTTP_401_UNAUTHORIZED: "请先登录",
    status.HTTP_403_FORBIDDEN: "禁止访问",
    status.HTTP_404_NOT_FOUND: "请求的资源不存在",
    status.HTTP_405_METHOD_NOT_ALLOWED: "请求方法不被允许",
    status.HTTP_409_CONFLICT: "请求与当前资源状态冲突",
    status.HTTP_422_UNPROCESSABLE_CONTENT: "请求参数验证失败",
}


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )
    app.add_exception_handler(
        StarletteHTTPException,
        http_exception_handler,
    )
    app.add_exception_handler(Exception, unhandled_exception_handler)


async def app_exception_handler(
    _request: Request,
    exception: Exception,
) -> JSONResponse:
    app_exception = cast(AppException, exception)

    response = _create_error_response(
        status_code=app_exception.status_code,
        code=app_exception.code,
        message=app_exception.message,
    )

    return response


async def validation_exception_handler(
    _request: Request,
    exception: Exception,
) -> JSONResponse:
    validation_exception = cast(RequestValidationError, exception)

    details = [
        {
            "field": ".".join(str(part) for part in error["loc"]),
            "type": error["type"],
        }
        for error in validation_exception.errors()
    ]

    error = RequestValidationAppException()

    response = _create_error_response(
        status_code=error.status_code,
        code=error.code,
        message=error.message,
        details=details,
    )

    return response


async def http_exception_handler(
    _request: Request,
    exception: Exception,
) -> JSONResponse:
    http_exception = cast(StarletteHTTPException, exception)

    error = HttpRequestException()
    code = f"HTTP_{http_exception.status_code}"
    message = HTTP_ERROR_MESSAGES.get(http_exception.status_code, error.message)

    response = _create_error_response(
        status_code=http_exception.status_code,
        code=code,
        message=message,
    )

    return response


async def unhandled_exception_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    logger.exception(
        "处理请求时发生未捕获异常",
        exc_info=exception,
        extra={"path": request.url.path},
    )

    error = InternalServerException()

    response = _create_error_response(
        status_code=error.status_code,
        code=error.code,
        message=error.message,
    )

    return response


def _create_error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    details: list[dict[str, Any]] | None = None,
) -> JSONResponse:
    content: dict[str, Any] = {
        "code": code,
        "message": message,
    }

    if details is not None:
        content["details"] = details

    response = JSONResponse(status_code=status_code, content=content)

    return response
