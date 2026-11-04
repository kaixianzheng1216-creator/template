import uuid
from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Mapped
from sqlmodel import Session, col, delete, func, select

from app.contents.models import Content
from app.users.exceptions import (
    SelfDeletionError,
    SelfManagementError,
    UserNotFoundError,
)
from app.users.models import User
from app.users.schemas import (
    UserListRequest,
    UserProfileUpdateRequest,
    UserRoleUpdateRequest,
    UserStatusUpdateRequest,
)


def update_user_profile(
    *,
    user: User,
    request: UserProfileUpdateRequest,
    db: Session,
) -> User:
    user.sqlmodel_update(request.model_dump())

    db.commit()

    db.refresh(user)

    return user


def list_users(
    *,
    request: UserListRequest,
    db: Session,
) -> tuple[list[User], int]:
    search = request.search.strip()
    statement = select(User)

    if search:
        statement = statement.where(
            or_(
                col(User.name).icontains(search, autoescape=True),
                col(User.email).icontains(search, autoescape=True),
            )
        )

    if request.is_active is not None:
        statement = statement.where(User.is_active == request.is_active)

    count = db.exec(select(func.count()).select_from(statement.subquery())).one()

    sort_column: Mapped[str] | Mapped[datetime]

    if request.sort == "name":
        sort_column = col(User.name)
    else:
        sort_column = col(User.created_at)

    if request.order == "asc":
        sort_order = sort_column.asc()
    else:
        sort_order = sort_column.desc()

    statement = statement.order_by(sort_order, col(User.id))
    statement = statement.offset(request.skip).limit(request.limit)

    users = list(db.exec(statement).all())

    return users, count


def update_user_role(
    *,
    user_id: uuid.UUID,
    request: UserRoleUpdateRequest,
    current_user: User,
    db: Session,
) -> User:
    if user_id == current_user.id:
        raise SelfManagementError

    user = _get_user_for_update(user_id=user_id, db=db)

    user.is_admin = request.is_admin

    db.commit()

    db.refresh(user)

    return user


def update_user_status(
    *,
    user_id: uuid.UUID,
    request: UserStatusUpdateRequest,
    current_user: User,
    db: Session,
) -> User:
    if user_id == current_user.id:
        raise SelfManagementError

    user = _get_user_for_update(user_id=user_id, db=db)

    user.is_active = request.is_active

    if not request.is_active:
        user.auth_version += 1

    db.commit()

    db.refresh(user)

    return user


def delete_users(*, user_ids: list[uuid.UUID], current_user: User, db: Session) -> None:
    ids = set(user_ids)

    if current_user.id in ids:
        raise SelfDeletionError

    existing_ids = db.exec(
        select(User.id)
        .where(col(User.id).in_(ids))
        .order_by(col(User.id))
        .with_for_update()
    ).all()

    if len(existing_ids) != len(ids):
        raise UserNotFoundError

    db.exec(delete(Content).where(col(Content.owner_id).in_(ids)))
    db.exec(delete(User).where(col(User.id).in_(ids)))

    db.commit()


def _get_user_for_update(*, user_id: uuid.UUID, db: Session) -> User:
    user = db.get(User, user_id, with_for_update=True)

    if user is None:
        raise UserNotFoundError

    return user
