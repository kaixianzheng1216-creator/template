from typing import Annotated, cast

from fastapi import Depends
from fastapi.security import APIKeyCookie

from app import redis_keys
from app.auth.exceptions import InvalidSessionError, PermissionDeniedError
from app.auth.schemas import AuthSession
from app.database import DbDep
from app.redis import redis_client
from app.users.models import User

SESSION_COOKIE_NAME = "session"

session_cookie = APIKeyCookie(
    name=SESSION_COOKIE_NAME,
    scheme_name="SessionCookie",
    description="登录后由浏览器自动携带的会话 Cookie",
    auto_error=False,
)

SessionToken = Annotated[str | None, Depends(session_cookie)]


def get_current_user(db: DbDep, session_token: SessionToken) -> User:
    if session_token is None:
        raise InvalidSessionError

    session_json = redis_client.get(redis_keys.session(session_token))

    if session_json is None:
        raise InvalidSessionError

    session_data = AuthSession.model_validate_json(cast(str, session_json))

    user = db.get(User, session_data.user_id)

    if user is None or not user.is_active:
        raise InvalidSessionError

    if session_data.auth_version != user.auth_version:
        raise InvalidSessionError

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_admin(current_user: CurrentUser) -> User:
    if not current_user.is_admin:
        raise PermissionDeniedError

    return current_user


CurrentAdmin = Annotated[User, Depends(get_current_admin)]
