import logging
from collections.abc import Mapping
from typing import cast

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from redis.exceptions import RedisError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions import AppException
from app.schemas import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


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
    app.add_exception_handler(RedisError, redis_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)


async def app_exception_handler(
    _request: Request,
    exception: Exception,
) -> JSONResponse:
    app_exception = cast(AppException, exception)

    return _create_error_response(
        status_code=app_exception.status_code,
        code=app_exception.code,
        message=app_exception.message,
    )


async def validation_exception_handler(
    _request: Request,
    exception: Exception,
) -> JSONResponse:
    validation_exception = cast(RequestValidationError, exception)

    details: list[ErrorDetail] = []

    for error in validation_exception.errors():
        field_parts: list[str] = []

        for part in error["loc"]:
            field_parts.append(str(part))

        details.append(
            ErrorDetail(
                field=".".join(field_parts),
                type=error["type"],
            )
        )

    return _create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        code="REQUEST_VALIDATION_ERROR",
        message="请求参数验证失败",
        details=details,
    )


async def http_exception_handler(
    _request: Request,
    exception: Exception,
) -> JSONResponse:
    http_exception = cast(StarletteHTTPException, exception)

    return _create_error_response(
        status_code=http_exception.status_code,
        code=f"HTTP_{http_exception.status_code}",
        message=str(http_exception.detail),
        headers=http_exception.headers,
    )


async def redis_exception_handler(
    _request: Request, exception: Exception
) -> JSONResponse:
    logger.error("Redis operation failed: error_type=%s", type(exception).__name__)

    return _create_error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        code="AUTH_STORE_UNAVAILABLE",
        message="认证服务暂不可用，请稍后再试",
    )


async def unhandled_exception_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    logger.exception(
        "处理请求时发生未捕获异常",
        exc_info=exception,
        extra={"path": request.url.path},
    )

    return _create_error_response(
        status_code=AppException.status_code,
        code=AppException.code,
        message=AppException.message,
    )


def _create_error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    details: list[ErrorDetail] | None = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    content = ErrorResponse(code=code, message=message, details=details).model_dump(
        exclude_none=True
    )

    return JSONResponse(status_code=status_code, content=content, headers=headers)
