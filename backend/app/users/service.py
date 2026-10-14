from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash
from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    user = User.model_validate(
        user_create,
        update={"hashed_password": get_password_hash(user_create.password)},
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(*, session: Session, user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        extra_data["hashed_password"] = get_password_hash(user_data["password"])
    user.sqlmodel_update(user_data, update=extra_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(*, session: Session, username: str) -> User | None:
    return session.exec(select(User).where(User.username == username)).first()


def create_development_user(
    *, session: Session, username: str, password: str, full_name: str
) -> User:
    user = User(
        username=username,
        full_name=full_name,
        hashed_password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    return user
