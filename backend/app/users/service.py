import uuid

from sqlmodel import Session, col, func, select

from app.auth.exceptions import InsufficientPermissionsError
from app.core.security import get_password_hash, verify_password
from app.users.exceptions import (
    IncorrectPasswordError,
    PasswordUnchangedError,
    SuperuserSelfDeletionError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
)
from app.users.models import User
from app.users.schemas import (
    UpdatePassword,
    UserCreate,
    UserRegister,
    UserUpdate,
    UserUpdateMe,
)


def register_user(*, session: Session, user_in: UserRegister) -> User:
    user_create = UserCreate.model_validate(user_in)
    user = create_user(session=session, user_create=user_create)

    return user


def update_current_user(
    *,
    session: Session,
    current_user: User,
    user_in: UserUpdateMe,
) -> User:
    if user_in.username is not None:
        _ensure_username_available(
            session=session,
            username=user_in.username,
            excluded_user_id=current_user.id,
        )

    current_user.sqlmodel_update(user_in.model_dump(exclude_unset=True))

    session.add(current_user)

    session.commit()

    session.refresh(current_user)

    return current_user


def update_password(
    *,
    session: Session,
    current_user: User,
    password_in: UpdatePassword,
) -> None:
    verified, _ = verify_password(
        password_in.current_password,
        current_user.hashed_password,
    )

    if not verified:
        raise IncorrectPasswordError

    if password_in.current_password == password_in.new_password:
        raise PasswordUnchangedError

    current_user.hashed_password = get_password_hash(password_in.new_password)

    session.add(current_user)

    session.commit()


def delete_current_user(*, session: Session, current_user: User) -> None:
    if current_user.is_superuser:
        raise SuperuserSelfDeletionError

    _delete_user(session=session, user=current_user)


def list_users(*, session: Session, skip: int, limit: int) -> tuple[list[User], int]:
    statement = (
        select(User).order_by(col(User.created_at).desc()).offset(skip).limit(limit)
    )

    count_statement = select(func.count()).select_from(User)

    users = list(session.exec(statement).all())

    count = session.exec(count_statement).one()

    return users, count


def create_user(*, session: Session, user_create: UserCreate) -> User:
    _ensure_username_available(session=session, username=user_create.username)

    user = User.model_validate(
        user_create,
        update={"hashed_password": get_password_hash(user_create.password)},
    )

    session.add(user)

    session.commit()

    session.refresh(user)

    return user


def get_user_by_id(
    *,
    session: Session,
    current_user: User,
    user_id: uuid.UUID,
) -> User:
    if current_user.id == user_id:
        return current_user

    if not current_user.is_superuser:
        raise InsufficientPermissionsError

    user = session.get(User, user_id)

    if user is None:
        raise UserNotFoundError

    return user


def update_user(
    *,
    session: Session,
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> User:
    user = session.get(User, user_id)

    if user is None:
        raise UserNotFoundError

    if user_in.username is not None:
        _ensure_username_available(
            session=session,
            username=user_in.username,
            excluded_user_id=user.id,
        )

    user_data = user_in.model_dump(exclude_unset=True)

    extra_data = {}

    if "password" in user_data:
        extra_data["hashed_password"] = get_password_hash(user_data["password"])

    user.sqlmodel_update(user_data, update=extra_data)

    session.add(user)

    session.commit()

    session.refresh(user)

    return user


def delete_user(
    *,
    session: Session,
    current_user: User,
    user_id: uuid.UUID,
) -> None:
    user = session.get(User, user_id)

    if user is None:
        raise UserNotFoundError

    if user.id == current_user.id:
        raise SuperuserSelfDeletionError

    _delete_user(session=session, user=user)


def get_user_by_username(*, session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)

    user = session.exec(statement).first()

    return user


def create_development_user(
    *,
    session: Session,
    username: str,
    password: str,
    full_name: str,
) -> User:
    user = User(
        username=username,
        full_name=full_name,
        hashed_password=get_password_hash(password),
    )

    session.add(user)

    session.commit()

    return user


def _ensure_username_available(
    *,
    session: Session,
    username: str,
    excluded_user_id: uuid.UUID | None = None,
) -> None:
    existing_user = get_user_by_username(session=session, username=username)

    if existing_user is None:
        return

    if excluded_user_id is not None and existing_user.id == excluded_user_id:
        return

    raise UsernameAlreadyExistsError


def _delete_user(*, session: Session, user: User) -> None:
    session.delete(user)

    session.commit()
