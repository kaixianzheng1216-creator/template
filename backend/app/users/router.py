import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status

from app.auth.dependencies import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.schemas import PaginationRequest
from app.users import service
from app.users.schemas import (
    UpdatePassword,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/signup",
    response_model=UserPublic,
    summary="注册用户",
)
def register_user(
    session: SessionDep,
    user_in: Annotated[UserRegister, Body(description="用户注册信息")],
) -> UserPublic:
    user = service.register_user(session=session, user_in=user_in)

    response = UserPublic.model_validate(user)

    return response


@router.get(
    "/me",
    response_model=UserPublic,
    summary="获取当前用户",
)
def read_user_me(current_user: CurrentUser) -> UserPublic:
    response = UserPublic.model_validate(current_user)

    return response


@router.patch(
    "/me",
    response_model=UserPublic,
    summary="更新当前用户",
)
def update_user_me(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    user_in: Annotated[UserUpdateMe, Body(description="当前用户更新信息")],
) -> UserPublic:
    user = service.update_current_user(
        session=session,
        current_user=current_user,
        user_in=user_in,
    )

    response = UserPublic.model_validate(user)

    return response


@router.patch(
    "/me/password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="更新当前用户密码",
)
def update_password_me(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    body: Annotated[UpdatePassword, Body(description="密码更新信息")],
) -> None:
    service.update_password(
        session=session,
        current_user=current_user,
        password_in=body,
    )


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除当前用户",
)
def delete_user_me(
    session: SessionDep,
    current_user: CurrentUser,
) -> None:
    service.delete_current_user(session=session, current_user=current_user)


@router.get(
    "",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
    summary="分页获取用户列表",
)
def read_users(
    session: SessionDep,
    pagination: Annotated[PaginationRequest, Query()],
) -> UsersPublic:
    users, count = service.list_users(
        session=session,
        skip=pagination.skip,
        limit=pagination.limit,
    )

    response = UsersPublic(
        data=[UserPublic.model_validate(user) for user in users],
        count=count,
    )

    return response


@router.post(
    "",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
    summary="创建用户",
)
def create_user(
    *,
    session: SessionDep,
    user_in: Annotated[UserCreate, Body(description="新用户信息")],
) -> UserPublic:
    user = service.create_user(session=session, user_create=user_in)

    response = UserPublic.model_validate(user)

    return response


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    summary="获取指定用户",
)
def read_user_by_id(
    session: SessionDep,
    current_user: CurrentUser,
    user_id: Annotated[uuid.UUID, Path(description="用户 ID")],
) -> UserPublic:
    user = service.get_user_by_id(
        session=session,
        current_user=current_user,
        user_id=user_id,
    )

    response = UserPublic.model_validate(user)

    return response


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
    summary="更新指定用户",
)
def update_user(
    *,
    session: SessionDep,
    user_id: Annotated[uuid.UUID, Path(description="用户 ID")],
    user_in: Annotated[UserUpdate, Body(description="用户更新信息")],
) -> UserPublic:
    user = service.update_user(
        session=session,
        user_id=user_id,
        user_in=user_in,
    )

    response = UserPublic.model_validate(user)

    return response


@router.delete(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除指定用户",
)
def delete_user(
    session: SessionDep,
    current_user: CurrentUser,
    user_id: Annotated[uuid.UUID, Path(description="用户 ID")],
) -> None:
    service.delete_user(
        session=session,
        current_user=current_user,
        user_id=user_id,
    )
