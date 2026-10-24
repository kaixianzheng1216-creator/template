from typing import Annotated

from fastapi import APIRouter, Body, Path, Query

from app.auth.dependencies import CurrentAdmin
from app.users import service
from app.users.schemas import (
    UserListQuery,
    UserPublic,
    UserRoleUpdate,
    UsersPublic,
    UserStatusUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "",
    summary="分页获取用户列表",
)
def list_users(
    _current_admin: CurrentAdmin,
    user_query: Annotated[UserListQuery, Query()],
) -> UsersPublic:
    users, total = service.list_users(user_query=user_query)

    return UsersPublic(data=users, count=total)


@router.put(
    "/{user_id}/role",
    summary="更新用户角色",
)
def update_user_role(
    current_user: CurrentAdmin,
    user_id: Annotated[str, Path(max_length=255, description="Clerk 用户 ID")],
    role_update: Annotated[UserRoleUpdate, Body(description="用户角色")],
) -> UserPublic:
    return service.update_user_role(
        current_user=current_user,
        user_id=user_id,
        is_admin=role_update.is_admin,
    )


@router.put(
    "/{user_id}/status",
    summary="更新用户状态",
)
def update_user_status(
    current_user: CurrentAdmin,
    user_id: Annotated[str, Path(max_length=255, description="Clerk 用户 ID")],
    status_update: Annotated[UserStatusUpdate, Body(description="用户状态")],
) -> UserPublic:
    return service.update_user_status(
        current_user=current_user,
        user_id=user_id,
        banned=status_update.banned,
    )
