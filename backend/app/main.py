from fastapi import FastAPI
from fastapi.routing import APIRoute
from scalar_fastapi import add_scalar_reference
from starlette.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.exception_handlers import register_exception_handlers


def custom_generate_unique_id(route: APIRoute) -> str:
    operation_id = route.name

    if route.tags:
        operation_id = f"{route.tags[0]}-{route.name}"

    return operation_id


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

register_exception_handlers(app)

add_scalar_reference(app, route="/scalar")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_HOST],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
