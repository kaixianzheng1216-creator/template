from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.auth.exceptions import (
    InactiveUserError,
    InsufficientPermissionsError,
    InvalidCredentialsError,
)
from app.auth.schemas import TokenPayload
from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.users.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )

        token_data = TokenPayload(**payload)
    except InvalidTokenError, ValidationError:
        raise InvalidCredentialsError from None

    user = session.get(User, token_data.sub)

    if not user:
        raise InvalidCredentialsError

    if not user.is_active:
        raise InactiveUserError

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise InsufficientPermissionsError

    return current_user
