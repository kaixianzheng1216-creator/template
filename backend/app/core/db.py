from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.users import service as users_service
from app.users.models import User
from app.users.schemas import UserCreate

engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)


def init_db(session: Session) -> None:
    user = session.exec(
        select(User).where(User.username == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        users_service.create_user(session=session, user_create=user_in)
