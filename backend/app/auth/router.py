from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import service
from app.auth.dependencies import CurrentUser, SessionDep
from app.auth.schemas import Token
from app.core import security
from app.core.config import settings
from app.users.schemas import UserPublic

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = service.authenticate(
        session=session,
        username=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户已停用")

    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = Token(
        access_token=security.create_access_token(user.id, expires_delta=expires)
    )

    return token


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    return current_user
