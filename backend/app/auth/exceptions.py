from fastapi import status

from app.exceptions import AppError


class EmailCodeRateLimitError(AppError):
    """验证码发送频率超限。"""

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = "AUTH_EMAIL_RATE_LIMIT"
    message = "验证码发送频繁，请稍后重试"

    def __init__(self, *, retry_after: int) -> None:
        super().__init__(headers={"Retry-After": str(retry_after)})


class EmailSendError(AppError):
    """验证码邮件发送失败。"""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "AUTH_EMAIL_DELIVERY_FAILED"
    message = "邮件发送失败，请稍后重试"


class InvalidEmailCodeError(AppError):
    """邮箱验证码无效。"""

    status_code = status.HTTP_400_BAD_REQUEST
    code = "AUTH_INVALID_EMAIL_CODE"
    message = "验证码无效，请重新获取"


class InvalidCredentialsError(AppError):
    """登录凭证无效。"""

    status_code = status.HTTP_401_UNAUTHORIZED
    code = "AUTH_INVALID_CREDENTIALS"
    message = "登录信息无效，请重试"


class LoginLockedError(AppError):
    """连续登录失败触发临时锁定。"""

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = "AUTH_LOGIN_LOCKED"
    message = "登录失败次数过多，请稍后重试"

    def __init__(self, *, retry_after: int) -> None:
        super().__init__(headers={"Retry-After": str(retry_after)})


class PasswordResetLockedError(AppError):
    """密码验证失败触发临时锁定。"""

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = "AUTH_PASSWORD_RESET_LOCKED"
    message = "验证码错误次数过多，请稍后重试"

    def __init__(self, *, retry_after: int) -> None:
        super().__init__(headers={"Retry-After": str(retry_after)})


class InvalidSessionError(AppError):
    """登录会话无效。"""

    status_code = status.HTTP_401_UNAUTHORIZED
    code = "AUTH_INVALID_SESSION"
    message = "登录状态无效，请重新登录"


class PermissionDeniedError(AppError):
    """用户权限不足。"""

    status_code = status.HTTP_403_FORBIDDEN
    code = "AUTH_INSUFFICIENT_PERMISSIONS"
    message = "权限不足"
