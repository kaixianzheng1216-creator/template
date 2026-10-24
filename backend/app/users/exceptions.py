from fastapi import status

from app.exceptions import AppException


class UserNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    code = "USER_NOT_FOUND"
    message = "用户不存在"


class SelfManagementError(AppException):
    status_code = status.HTTP_409_CONFLICT
    code = "SELF_MANAGEMENT_FORBIDDEN"
    message = "不能修改自己的角色或状态"


class ClerkRequestError(AppException):
    status_code = status.HTTP_502_BAD_GATEWAY
    code = "CLERK_REQUEST_FAILED"
    message = "用户服务请求失败"


class ClerkUnavailableError(AppException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "CLERK_UNAVAILABLE"
    message = "用户服务暂时不可用"
