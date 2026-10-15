from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import service
from app.auth.dependencies import CurrentUser, SessionDep
from app.auth.schemas import Token
from app.users.schemas import UserPublic

router = APIRouter(tags=["login"])


@router.post(
    "/login/access-token",
    summary="使用用户名和密码登录",
)
def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    token = service.login(
        session=session,
        username=form_data.username,
        password=form_data.password,
    )

    return token


@router.post(
    "/login/test-token",
    summary="验证访问令牌",
)
def test_token(current_user: CurrentUser) -> UserPublic:
    response = UserPublic.model_validate(current_user)

    return response
