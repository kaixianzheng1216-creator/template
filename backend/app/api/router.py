from fastapi import APIRouter

from app.contents.router import router as contents_router
from app.health.router import router as health_router
from app.schemas import ErrorResponse
from app.users.router import router as users_router

api_router = APIRouter(
    responses={
        "default": {"model": ErrorResponse},
        422: {"model": ErrorResponse, "description": "请求参数验证失败"},
    }
)

api_router.include_router(users_router)
api_router.include_router(contents_router)
api_router.include_router(health_router)
