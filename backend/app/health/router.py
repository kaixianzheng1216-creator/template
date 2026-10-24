from fastapi import APIRouter
from sqlalchemy import text

from app.database import SessionDep

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/ready",
    include_in_schema=False,
    summary="检查服务就绪状态",
)
def readiness(session: SessionDep) -> bool:
    session.execute(text("SELECT 1"))
    return True
