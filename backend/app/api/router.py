from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.core.config import settings
from app.health.router import router as health_router
from app.items.router import router as items_router
from app.users.development_router import router as development_router
from app.users.router import router as users_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(health_router)
api_router.include_router(items_router)

if settings.FASTAPI_ENV == "development":
    api_router.include_router(development_router)
