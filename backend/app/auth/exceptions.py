from fastapi import status

from app.exceptions import AppError


class EmailCodeRateLimitError(AppError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = "AUTH_EMAIL_RATE_LIMIT"
    detail = "发送请求过于频繁，请稍后重试"

    def __init__(self, *, retry_after: int) -> None:
        super().__init__(headers={"Retry-After": str(retry_after)})


class EmailSendError(AppError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "AUTH_EMAIL_DELIVERY_FAILED"
    detail = "邮件发送失败，请稍后重试"


class InvalidEmailCodeError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "AUTH_INVALID_EMAIL_CODE"
    detail = "验证码错误或已过期"


class InvalidCredentialsError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "AUTH_INVALID_CREDENTIALS"
    detail = "登录信息无效，请重试"


class LoginLockedError(AppError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = "AUTH_LOGIN_LOCKED"
    detail = "登录失败次数过多，请稍后重试"

    def __init__(self, *, retry_after: int) -> None:
        super().__init__(headers={"Retry-After": str(retry_after)})


class PasswordResetLockedError(AppError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = "AUTH_PASSWORD_RESET_LOCKED"
    detail = "验证码错误次数过多，请稍后重试"

    def __init__(self, *, retry_after: int) -> None:
        super().__init__(headers={"Retry-After": str(retry_after)})


class InvalidSessionError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "AUTH_INVALID_SESSION"
    detail = "登录状态无效，请重新登录"


class PermissionDeniedError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "AUTH_INSUFFICIENT_PERMISSIONS"
    detail = "权限不足"
