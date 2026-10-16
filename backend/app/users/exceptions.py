from fastapi import status

from app.exceptions import AppException


class UserNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    code = "USER_NOT_FOUND"
    message = "用户不存在"


class UsernameAlreadyExistsError(AppException):
    status_code = status.HTTP_409_CONFLICT
    code = "USERNAME_ALREADY_EXISTS"
    message = "该用户名已存在"


class IncorrectPasswordError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "INCORRECT_PASSWORD"
    message = "当前密码错误"


class PasswordUnchangedError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "PASSWORD_UNCHANGED"
    message = "新密码不能与当前密码相同"


class SuperuserSelfDeletionError(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "SUPERUSER_SELF_DELETION_FORBIDDEN"
    message = "管理员不能删除自己的账号"
