from collections.abc import Callable
from datetime import UTC, datetime
from http import HTTPStatus

from clerk_backend_api.models import (
    ClerkBaseError,
    GetUserListRequest,
    GetUsersCountRequest,
    User,
)
from httpx import HTTPError

from app.auth.service import AuthenticatedUser
from app.clerk import clerk
from app.users.exceptions import (
    ClerkRequestError,
    SelfManagementError,
    UserNotFoundError,
)
from app.users.schemas import UserListQuery, UserPublic


def list_users(*, user_query: UserListQuery) -> tuple[list[UserPublic], int]:
    name = user_query.full_name.strip() or None
    email = user_query.email.strip() or None

    sort_field = "created_at"

    if user_query.sort == "name":
        sort_field = "first_name"

    sort_prefix = "-"

    if user_query.order == "asc":
        sort_prefix = "+"

    count_request = GetUsersCountRequest(
        name_query=name,
        email_address_query=email,
        banned=user_query.banned,
    )

    list_request = GetUserListRequest(
        name_query=name,
        email_address_query=email,
        banned=user_query.banned,
        offset=user_query.skip,
        limit=user_query.limit,
        order_by=f"{sort_prefix}{sort_field}",
    )

    total = _call_clerk(lambda: clerk.users.count(request=count_request)).total_count

    users = _call_clerk(lambda: clerk.users.list(request=list_request))

    public_users: list[UserPublic] = []

    for user in users:
        public_users.append(_to_user_public(user))

    return public_users, total


def update_user_role(
    *,
    current_user: AuthenticatedUser,
    user_id: str,
    is_admin: bool,
) -> UserPublic:
    if user_id == current_user.user_id:
        raise SelfManagementError

    role = "member"

    if is_admin:
        role = "admin"

    user = _call_clerk(
        lambda: clerk.users.update_metadata(
            user_id=user_id,
            public_metadata={"role": role},
        )
    )
    return _to_user_public(user)


def update_user_status(
    *,
    current_user: AuthenticatedUser,
    user_id: str,
    banned: bool,
) -> UserPublic:
    if user_id == current_user.user_id:
        raise SelfManagementError

    if banned:
        user = _call_clerk(lambda: clerk.users.ban(user_id=user_id))
    else:
        user = _call_clerk(lambda: clerk.users.unban(user_id=user_id))

    return _to_user_public(user)


def _call_clerk[ResultT](
    operation: Callable[[], ResultT],
) -> ResultT:
    try:
        return operation()
    except ClerkBaseError as error:
        if error.status_code == HTTPStatus.NOT_FOUND:
            raise UserNotFoundError from error
        raise ClerkRequestError from error
    except HTTPError as error:
        raise ClerkRequestError from error


def _to_user_public(user: User) -> UserPublic:
    email = None

    for address in user.email_addresses:
        if address.id == user.primary_email_address_id:
            email = address.email_address
            break

    name_parts: list[str] = []

    if user.first_name:
        name_parts.append(user.first_name)

    if user.last_name:
        name_parts.append(user.last_name)

    full_name = " ".join(name_parts) or None

    return UserPublic(
        id=user.id,
        email=email,
        full_name=full_name,
        banned=user.banned,
        is_admin=user.public_metadata.get("role") == "admin",
        created_at=datetime.fromtimestamp(user.created_at / 1000, tz=UTC),
    )
