from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)


def get_db() -> Generator[Session]:
    with Session(engine) as db:
        yield db


DbDep = Annotated[Session, Depends(get_db)]
