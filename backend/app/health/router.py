from fastapi import APIRouter
from sqlmodel import select

from app.database import DbDep
from app.redis import redis_client

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/ready",
    include_in_schema=False,
    summary="检查服务就绪状态",
)
def readiness(db: DbDep) -> bool:
    db.exec(select(1))

    redis_client.ping()

    return True
