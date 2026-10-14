from typing import Any

from sqlmodel import SQLModel


class Message(SQLModel):
    message: str


class ErrorResponse(SQLModel):
    code: str
    message: str


class ValidationErrorResponse(ErrorResponse):
    details: list[dict[str, Any]]
