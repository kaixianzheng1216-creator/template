from sqlmodel import Session

from app.core.security import verify_password
from app.users import service as users_service
from app.users.models import User

# 用户不存在时仍执行密码校验，降低基于响应时间推测用户名的风险。
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


def authenticate(*, session: Session, username: str, password: str) -> User | None:
    user = users_service.get_user_by_username(session=session, username=username)

    if not user:
        verify_password(password, DUMMY_HASH)
        return None

    verified, updated_password_hash = verify_password(password, user.hashed_password)

    if not verified:
        return None

    if updated_password_hash:
        user.hashed_password = updated_password_hash
        session.add(user)
        session.commit()
        session.refresh(user)

    return user
