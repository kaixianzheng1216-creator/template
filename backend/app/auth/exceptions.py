from fastapi import status

from app.exceptions import AppException


class InvalidCredentialsError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "AUTH_INVALID_CREDENTIALS"
    message = "请先登录"


class InsufficientPermissionsError(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "AUTH_INSUFFICIENT_PERMISSIONS"
    message = "当前用户权限不足"
