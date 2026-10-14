from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.auth.dependencies import SessionDep
from app.users import service
from app.users.models import User
from app.users.schemas import UserPublic

router = APIRouter(tags=["private"], prefix="/private")


class PrivateUserCreate(BaseModel):
    username: str
    password: str
    full_name: str


@router.post("/users/", response_model=UserPublic)
def create_user(user_in: PrivateUserCreate, session: SessionDep) -> Any:
    user: User = service.create_development_user(
        session=session,
        username=user_in.username,
        password=user_in.password,
        full_name=user_in.full_name,
    )

    return user
