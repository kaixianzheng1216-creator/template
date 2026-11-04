from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute
from scalar_fastapi import add_scalar_reference
from sqlmodel import Session
from starlette.concurrency import run_in_threadpool

from app.api.exception_handlers import register_error_handlers
from app.api.router import api_router
from app.config import settings
from app.database import engine
from app.initial_data import initialize_admin
from app.redis import redis_client


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    try:
        await run_in_threadpool(redis_client.ping)

        with Session(engine) as db:
            initialize_admin(db=db)
        yield
    finally:
        redis_client.close()


def generate_operation_id(route: APIRoute) -> str:
    operation_id = route.name

    if route.tags:
        operation_id = f"{route.tags[0]}-{route.name}"

    return operation_id


app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json",
    generate_unique_id_function=generate_operation_id,
)

register_error_handlers(app)

add_scalar_reference(app)

app.include_router(api_router, prefix="/api/v1")
