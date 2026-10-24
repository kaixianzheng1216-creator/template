from typing import Annotated

from fastapi import Depends, Request

from app.auth import service as auth_service
from app.auth.exceptions import InsufficientPermissionsError
from app.auth.service import AuthenticatedUser


def get_current_user(request: Request) -> AuthenticatedUser:
    return auth_service.authenticate_request(request)


CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]


def get_current_admin(current_user: CurrentUser) -> AuthenticatedUser:
    if not current_user.is_admin:
        raise InsufficientPermissionsError

    return current_user


CurrentAdmin = Annotated[AuthenticatedUser, Depends(get_current_admin)]
