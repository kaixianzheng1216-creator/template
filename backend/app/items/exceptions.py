from fastapi import status

from app.exceptions import AppException


class ItemNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    code = "ITEM_NOT_FOUND"
    message = "内容不存在"


class ItemAccessDeniedError(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "ITEM_ACCESS_DENIED"
    message = "没有足够的权限"
