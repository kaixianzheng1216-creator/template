from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session

from app.auth.service import password_hasher
from app.config import settings
from app.users.models import User


def initialize_admin(*, db: Session) -> None:
    """创建初始管理员，保留已有账号。"""
    statement = (
        insert(User)
        .values(
            email=settings.ADMIN_EMAIL,
            name="管理员",
            password_hash=password_hasher.hash(
                settings.ADMIN_PASSWORD.get_secret_value()
            ),
            is_admin=True,
        )
        .on_conflict_do_nothing(index_elements=["email"])
    )

    db.exec(statement)

    db.commit()
