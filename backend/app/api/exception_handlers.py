import logging
from collections.abc import Mapping
from typing import cast

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import TimeoutError as RedisTimeoutError
from starlette.exceptions import HTTPException

from app.exceptions import AppError
from app.schemas import ErrorResponse, ValidationErrorDetail

logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, handle_validation_error)

    app.add_exception_handler(AppError, handle_app_error)

    app.add_exception_handler(HTTPException, handle_http_error)

    app.add_exception_handler(RedisConnectionError, handle_redis_error)

    app.add_exception_handler(RedisTimeoutError, handle_redis_error)

    app.add_exception_handler(Exception, handle_unexpected_error)


async def handle_validation_error(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    error = cast(RequestValidationError, exc)

    details: list[ValidationErrorDetail] = []

    for issue in error.errors():
        field_parts: list[str] = []

        for part in issue["loc"]:
            field_parts.append(str(part))

        details.append(
            ValidationErrorDetail(field=".".join(field_parts), type=issue["type"])
        )

    return _create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        code="REQUEST_VALIDATION_ERROR",
        message="请求参数无效",
        details=details,
    )


async def handle_app_error(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    error = cast(AppError, exc)

    return _create_error_response(
        status_code=error.status_code,
        code=error.code,
        message=error.detail,
        headers=error.headers,
    )


async def handle_http_error(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    error = cast(HTTPException, exc)
    message = str(error.detail)

    if error.status_code == status.HTTP_404_NOT_FOUND and message == "Not Found":
        message = "接口不存在"
    elif (
        error.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        and message == "Method Not Allowed"
    ):
        message = "请求方法不支持"

    return _create_error_response(
        status_code=error.status_code,
        code=f"HTTP_{error.status_code}",
        message=message,
        headers=error.headers,
    )


async def handle_redis_error(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.error("Redis 连接失败：%s", type(exc).__name__)

    return _create_error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        code="AUTH_STORE_UNAVAILABLE",
        message="认证服务暂不可用，请稍后重试",
    )


async def handle_unexpected_error(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "请求处理异常",
        exc_info=exc,
        extra={"path": request.url.path},
    )

    return _create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="INTERNAL_SERVER_ERROR",
        message="服务器内部错误",
    )


def _create_error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    details: list[ValidationErrorDetail] | None = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    error = ErrorResponse(code=code, message=message, details=details)

    return JSONResponse(
        status_code=status_code,
        content=error.model_dump(exclude_none=True),
        headers=headers,
    )
