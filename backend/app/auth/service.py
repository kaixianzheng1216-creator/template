from dataclasses import dataclass

from clerk_backend_api.security.types import AuthenticateRequestOptions
from fastapi import Request

from app.auth.exceptions import InvalidCredentialsError
from app.clerk import clerk
from app.config import settings


@dataclass(frozen=True)
class AuthenticatedUser:
    user_id: str
    is_admin: bool


def authenticate_request(request: Request) -> AuthenticatedUser:
    auth_state = clerk.authenticate_request(
        request,
        AuthenticateRequestOptions(
            accepts_token=["session_token"],
            authorized_parties=[settings.FRONTEND_URL],
        ),
    )

    if not auth_state.is_authenticated or auth_state.payload is None:
        raise InvalidCredentialsError

    user_id = auth_state.payload.get("sub")

    if not isinstance(user_id, str):
        raise InvalidCredentialsError

    metadata = auth_state.payload.get("metadata")

    role = None

    if isinstance(metadata, dict):
        role = metadata.get("role")

    return AuthenticatedUser(
        user_id=user_id,
        is_admin=role == "admin",
    )
