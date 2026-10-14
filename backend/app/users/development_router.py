from typing import Annotated

from fastapi import APIRouter, Body

from app.auth.dependencies import SessionDep
from app.users import service
from app.users.schemas import PrivateUserCreate, UserPublic

router = APIRouter(tags=["private"], prefix="/private")


@router.post(
    "/users",
    response_model=UserPublic,
    summary="创建开发测试用户",
)
def create_user(
    user_in: Annotated[PrivateUserCreate, Body(description="测试用户信息")],
    session: SessionDep,
) -> UserPublic:
    user = service.create_development_user(
        session=session,
        username=user_in.username,
        password=user_in.password,
        full_name=user_in.full_name,
    )

    response = UserPublic.model_validate(user)

    return response
