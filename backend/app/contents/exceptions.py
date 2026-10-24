from fastapi import status

from app.exceptions import AppException


class ContentNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    code = "CONTENT_NOT_FOUND"
    message = "内容不存在"
