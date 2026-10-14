from fastapi import status

from app.exceptions import AppException


class InvalidCredentialsError(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "AUTH_INVALID_CREDENTIALS"
    message = "无法验证登录凭证"


class LoginFailedError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "AUTH_LOGIN_FAILED"
    message = "用户名或密码错误"


class InactiveUserError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "AUTH_USER_INACTIVE"
    message = "用户已停用"


class InsufficientPermissionsError(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "AUTH_INSUFFICIENT_PERMISSIONS"
    message = "当前用户权限不足"
