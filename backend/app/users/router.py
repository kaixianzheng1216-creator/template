import uuid
from typing import Annotated

from fastapi import APIRouter, Query, status

from app.auth.dependencies import CurrentAdmin, CurrentUser
from app.database import DbDep
from app.users import service
from app.users.schemas import (
    UserBatchDeleteRequest,
    UserListRequest,
    UserListResponse,
    UserProfileUpdateRequest,
    UserResponse,
    UserRoleUpdateRequest,
    UserStatusUpdateRequest,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    summary="获取当前用户",
)
def get_current_user(current_user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.put(
    "/me",
    summary="更新当前用户资料",
)
def update_current_user(
    request: UserProfileUpdateRequest,
    current_user: CurrentUser,
    db: DbDep,
) -> UserResponse:
    user = service.update_user_profile(
        user=current_user,
        request=request,
        db=db,
    )

    return UserResponse.model_validate(user)


@router.get(
    "",
    summary="分页查询用户",
)
def list_users(
    request: Annotated[UserListRequest, Query()],
    _current_admin: CurrentAdmin,
    db: DbDep,
) -> UserListResponse:
    users, count = service.list_users(request=request, db=db)

    return UserListResponse.model_validate({"data": users, "count": count})


@router.put(
    "/{user_id}/role",
    summary="更新用户角色",
)
def update_user_role(
    user_id: uuid.UUID,
    request: UserRoleUpdateRequest,
    current_user: CurrentAdmin,
    db: DbDep,
) -> UserResponse:
    user = service.update_user_role(
        user_id=user_id,
        request=request,
        current_user=current_user,
        db=db,
    )

    return UserResponse.model_validate(user)


@router.put(
    "/{user_id}/status",
    summary="更新用户状态",
)
def update_user_status(
    user_id: uuid.UUID,
    request: UserStatusUpdateRequest,
    current_user: CurrentAdmin,
    db: DbDep,
) -> UserResponse:
    user = service.update_user_status(
        user_id=user_id,
        request=request,
        current_user=current_user,
        db=db,
    )

    return UserResponse.model_validate(user)


@router.post(
    "/bulk-delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="批量删除用户及其内容",
)
def delete_users(
    request: UserBatchDeleteRequest,
    current_user: CurrentAdmin,
    db: DbDep,
) -> None:
    service.delete_users(user_ids=request.ids, current_user=current_user, db=db)
