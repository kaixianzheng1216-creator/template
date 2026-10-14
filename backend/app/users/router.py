import uuid

from fastapi import APIRouter, Depends

from app.auth.dependencies import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.schemas import Message
from app.users import service
from app.users.constants import UserMessage
from app.users.models import User
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


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> UsersPublic:
    users, count = service.list_users(session=session, skip=skip, limit=limit)

    response = UsersPublic(
        data=[UserPublic.model_validate(user) for user in users],
        count=count,
    )

    return response


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> User:
    user = service.create_user(session=session, user_create=user_in)

    return user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *,
    session: SessionDep,
    user_in: UserUpdateMe,
    current_user: CurrentUser,
) -> User:
    user = service.update_current_user(
        session=session,
        current_user=current_user,
        user_in=user_in,
    )

    return user


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *,
    session: SessionDep,
    body: UpdatePassword,
    current_user: CurrentUser,
) -> Message:
    service.update_password(
        session=session,
        current_user=current_user,
        password_in=body,
    )

    response = Message(message=UserMessage.PASSWORD_UPDATED)

    return response


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> User:
    return current_user


@router.delete("/me", response_model=Message)
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Message:
    service.delete_current_user(session=session, current_user=current_user)

    response = Message(message=UserMessage.USER_DELETED)

    return response


@router.post("/signup", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserRegister) -> User:
    user = service.register_user(session=session, user_in=user_in)

    return user


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> User:
    user = service.get_user_by_id(
        session=session,
        current_user=current_user,
        user_id=user_id,
    )

    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def update_user(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> User:
    user = service.update_user(
        session=session,
        user_id=user_id,
        user_in=user_in,
    )

    return user


@router.delete(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
)
def delete_user(
    session: SessionDep,
    current_user: CurrentUser,
    user_id: uuid.UUID,
) -> Message:
    service.delete_user(
        session=session,
        current_user=current_user,
        user_id=user_id,
    )

    response = Message(message=UserMessage.USER_DELETED)

    return response
