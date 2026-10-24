from fastapi import APIRouter

from app.health.router import router as health_router
from app.items.router import router as items_router
from app.schemas import ErrorResponse
from app.users.router import router as users_router

api_router = APIRouter(
    responses={
        "default": {"model": ErrorResponse},
        422: {"model": ErrorResponse, "description": "请求参数验证失败"},
    }
)

api_router.include_router(users_router)
api_router.include_router(items_router)
api_router.include_router(health_router)
