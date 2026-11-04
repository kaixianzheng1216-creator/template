from fastapi import status

from app.exceptions import AppError


class ContentNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "CONTENT_NOT_FOUND"
    detail = "内容不存在"
