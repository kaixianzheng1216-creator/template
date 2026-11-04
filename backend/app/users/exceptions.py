from fastapi import status

from app.exceptions import AppError


class UserNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "USER_NOT_FOUND"
    detail = "用户不存在"


class UserSelfManagementError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "USER_SELF_MANAGEMENT_FORBIDDEN"
    detail = "不能修改自己的角色或状态"


class UserSelfDeletionError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "USER_SELF_DELETION_FORBIDDEN"
    detail = "不能删除自己的账号"
