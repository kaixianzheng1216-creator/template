from fastapi import APIRouter

from app.health.schemas import HealthResponse

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get(
    "/health-check",
    summary="检查服务健康状态",
)
async def health_check() -> HealthResponse:
    response = HealthResponse(True)

    return response
