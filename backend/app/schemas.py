from pydantic import BaseModel


class ErrorDetail(BaseModel):
    field: str
    type: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] | None = None
