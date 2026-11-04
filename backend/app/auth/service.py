import hashlib
import hmac
import secrets
from pathlib import Path
from typing import cast

from pwdlib import PasswordHash
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, col, select

from app import redis_keys
from app.auth.email import send_verification_email
from app.auth.exceptions import (
    EmailCodeRateLimitError,
    InvalidCredentialsError,
    InvalidEmailCodeError,
    LoginLockedError,
    PasswordResetLockedError,
)
from app.auth.schemas import (
    AuthPurpose,
    AuthSession,
    EmailCodeLoginRequest,
    EmailCodePurpose,
    EmailCodeSendRequest,
    PasswordLoginRequest,
)
from app.config import settings
from app.redis import redis_client
from app.users.models import User

EMAIL_CODE_INTERVAL_SECONDS = 60

EMAIL_CODE_TTL_SECONDS = 600

FAILURE_WINDOW_SECONDS = 600

MAX_EMAIL_CODE_FAILURES = 5

MAX_PASSWORD_LOGIN_FAILURES = 5

LOCK_DURATION_SECONDS = 900

_VERIFY_AND_DELETE_EMAIL_CODE_SCRIPT = (
    Path(__file__).parent / "lua" / "verify_and_delete_email_code.lua"
).read_text(encoding="utf-8")

_UPDATE_FAILURE_COUNT_SCRIPT = (
    Path(__file__).parent / "lua" / "update_failure_count.lua"
).read_text(encoding="utf-8")

password_hasher = PasswordHash.recommended()

DUMMY_PASSWORD_HASH = password_hasher.hash("not-the-user-password")


def send_email_code(*, request: EmailCodeSendRequest, db: Session) -> None:
    email = request.email
    purpose = request.purpose

    _check_failure_limit(email=email, purpose=purpose)

    send_interval_key = redis_keys.email_send_interval(email, purpose)
    can_send_code = redis_client.set(
        send_interval_key, "1", ex=EMAIL_CODE_INTERVAL_SECONDS, nx=True
    )

    if not can_send_code:
        retry_after = cast(int, redis_client.ttl(send_interval_key))
        raise EmailCodeRateLimitError(retry_after=max(1, retry_after))

    user = db.exec(select(User).where(User.email == email)).one_or_none()

    if user is not None and not user.is_active:
        return

    if user is None and purpose == "password_reset":
        return

    email_code = f"{secrets.randbelow(1_000_000):06d}"

    email_code_hash = _hash_email_code(
        email=email, purpose=purpose, email_code=email_code
    )

    email_code_key = redis_keys.email_code(email, purpose)

    redis_client.set(email_code_key, email_code_hash, ex=EMAIL_CODE_TTL_SECONDS)

    send_verification_email(
        email=email,
        purpose=purpose,
        email_code=email_code,
        expires_in_seconds=EMAIL_CODE_TTL_SECONDS,
    )


def login_with_email_code(
    *, request: EmailCodeLoginRequest, db: Session
) -> AuthSession:
    email = request.email
    email_code = request.code

    _verify_and_delete_email_code(
        email=email, purpose="email_login", email_code=email_code
    )

    db.exec(
        insert(User)
        .values(email=email, name=email.split("@", 1)[0])
        .on_conflict_do_nothing(index_elements=["email"])
    )

    user = db.exec(select(User).where(User.email == email)).one_or_none()

    if user is None or not user.is_active:
        _update_failure_count(email=email, purpose="email_login", success=False)
        raise InvalidCredentialsError

    session_data = AuthSession(user_id=user.id, auth_version=user.auth_version)

    _update_failure_count(email=email, purpose="email_login", success=True)

    db.commit()

    return session_data


def login_with_password(*, request: PasswordLoginRequest, db: Session) -> AuthSession:
    email = request.email
    password = request.password

    _check_failure_limit(email=email, purpose="password_login")

    user = db.exec(select(User).where(User.email == email)).one_or_none()

    if user is None or not user.password_hash:
        password_hasher.verify(password, DUMMY_PASSWORD_HASH)
        _update_failure_count(email=email, purpose="password_login", success=False)
        raise InvalidCredentialsError

    is_password_valid = password_hasher.verify(password, user.password_hash)

    if not is_password_valid or not user.is_active:
        _update_failure_count(email=email, purpose="password_login", success=False)
        raise InvalidCredentialsError

    _update_failure_count(email=email, purpose="password_login", success=True)

    return AuthSession(user_id=user.id, auth_version=user.auth_version)


def login_dev_admin(*, db: Session) -> AuthSession:
    user = db.exec(
        select(User).where(
            User.email == settings.ADMIN_EMAIL,
            col(User.is_admin).is_(True),
            col(User.is_active).is_(True),
        )
    ).one_or_none()

    if user is None:
        raise InvalidCredentialsError

    return AuthSession(user_id=user.id, auth_version=user.auth_version)


def set_password_with_email_code(
    *, email: str, email_code: str, password: str, db: Session
) -> AuthSession:
    _verify_and_delete_email_code(
        email=email, purpose="password_reset", email_code=email_code
    )

    password_hash = password_hasher.hash(password)

    updated_user = db.exec(
        update(User)
        .where(col(User.email) == email, col(User.is_active).is_(True))
        .values(
            password_hash=password_hash,
            auth_version=col(User.auth_version) + 1,
        )
        .returning(col(User.id), col(User.auth_version)),
    ).one_or_none()

    if updated_user is None:
        _update_failure_count(email=email, purpose="password_reset", success=False)

        raise InvalidEmailCodeError

    session_data = AuthSession(
        user_id=updated_user.id, auth_version=updated_user.auth_version
    )

    _update_failure_count(email=email, purpose="password_reset", success=True)

    db.commit()

    redis_client.delete(
        redis_keys.auth_failure_count(email, "email_login"),
        redis_keys.auth_failure_count(email, "password_login"),
    )

    return session_data


def create_session(*, session_data: AuthSession) -> str:
    session_token = secrets.token_urlsafe(32)

    redis_client.set(
        redis_keys.session(session_token),
        session_data.model_dump_json(),
        ex=settings.SESSION_MAX_AGE_SECONDS,
    )

    return session_token


def delete_session(*, session_token: str | None) -> None:
    if session_token is not None:
        redis_client.delete(redis_keys.session(session_token))


def _check_failure_limit(*, email: str, purpose: AuthPurpose) -> None:
    failure_count_key = redis_keys.auth_failure_count(email, purpose)
    with redis_client.pipeline() as pipeline:
        pipeline.get(failure_count_key)
        pipeline.ttl(failure_count_key)
        failure_count, retry_after = pipeline.execute()

    if failure_count is None:
        return

    if purpose == "password_login":
        max_failures = MAX_PASSWORD_LOGIN_FAILURES
    else:
        max_failures = MAX_EMAIL_CODE_FAILURES

    if int(failure_count) < max_failures:
        return

    retry_after = max(1, retry_after)

    if purpose == "password_reset":
        raise PasswordResetLockedError(retry_after=retry_after)

    raise LoginLockedError(retry_after=retry_after)


def _hash_email_code(*, email: str, purpose: EmailCodePurpose, email_code: str) -> str:
    return hmac.new(
        settings.EMAIL_CODE_SECRET.get_secret_value().encode(),
        f"{purpose}:{email}:{email_code}".encode(),
        hashlib.sha256,
    ).hexdigest()


def _verify_and_delete_email_code(
    *, email: str, purpose: EmailCodePurpose, email_code: str
) -> None:
    _check_failure_limit(email=email, purpose=purpose)

    email_code_hash = _hash_email_code(
        email=email, purpose=purpose, email_code=email_code
    )

    email_code_key = redis_keys.email_code(email, purpose)

    is_email_code_valid = redis_client.eval(
        _VERIFY_AND_DELETE_EMAIL_CODE_SCRIPT,
        1,
        email_code_key,
        email_code_hash,
    )

    if is_email_code_valid:
        return

    _update_failure_count(email=email, purpose=purpose, success=False)
    raise InvalidEmailCodeError


def _update_failure_count(*, email: str, purpose: AuthPurpose, success: bool) -> None:
    if purpose == "password_login":
        max_failures = MAX_PASSWORD_LOGIN_FAILURES
    else:
        max_failures = MAX_EMAIL_CODE_FAILURES

    failure_count_key = redis_keys.auth_failure_count(email, purpose)

    script_result: object = redis_client.eval(
        _UPDATE_FAILURE_COUNT_SCRIPT,
        1,
        failure_count_key,
        int(success),
        max_failures,
        LOCK_DURATION_SECONDS,
        FAILURE_WINDOW_SECONDS,
    )

    retry_after = cast(int, script_result)

    if retry_after <= 0:
        return

    if purpose == "password_reset":
        raise PasswordResetLockedError(retry_after=retry_after)

    raise LoginLockedError(retry_after=retry_after)
