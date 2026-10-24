from fastapi import FastAPI
from fastapi.routing import APIRoute
from scalar_fastapi import add_scalar_reference

from app.api.exception_handlers import register_exception_handlers
from app.api.router import api_router
from app.config import settings


def generate_operation_id(route: APIRoute) -> str:
    operation_id = route.name

    if route.tags:
        operation_id = f"{route.tags[0]}-{route.name}"

    return operation_id


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json",
    generate_unique_id_function=generate_operation_id,
)

register_exception_handlers(app)

add_scalar_reference(app, route="/scalar")

app.include_router(api_router, prefix="/api/v1")
