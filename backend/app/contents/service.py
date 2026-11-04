import uuid
from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Mapped
from sqlmodel import Session, col, delete, func, select
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.contents.exceptions import ContentNotFoundError
from app.contents.models import Content
from app.contents.schemas import (
    AdminContentListRequest,
    ContentBatchDeleteRequest,
    ContentCreateRequest,
    ContentListRequest,
    ContentUpdateRequest,
)
from app.users.models import User


def list_contents(
    *,
    request: ContentListRequest,
    owner_id: uuid.UUID,
    db: Session,
) -> tuple[list[Content], int]:
    statement = select(Content).where(Content.owner_id == owner_id)

    return _paginate_contents(statement=statement, request=request, db=db)


def create_content(
    *,
    request: ContentCreateRequest,
    owner_id: uuid.UUID,
    db: Session,
) -> Content:
    content = Content.model_validate(
        request,
        update={"owner_id": owner_id},
    )

    db.add(content)
    db.commit()
    db.refresh(content)

    return content


def update_content(
    *,
    content_id: uuid.UUID,
    request: ContentUpdateRequest,
    owner_id: uuid.UUID | None,
    db: Session,
) -> Content:
    statement = select(Content).where(Content.id == content_id)

    if owner_id is not None:
        statement = statement.where(Content.owner_id == owner_id)

    content = db.exec(statement).one_or_none()

    if content is None:
        raise ContentNotFoundError

    content.sqlmodel_update(request.model_dump())

    db.commit()
    db.refresh(content)

    return content


def delete_contents(
    *,
    request: ContentBatchDeleteRequest,
    owner_id: uuid.UUID | None,
    db: Session,
) -> None:
    ids = set(request.ids)

    statement = delete(Content).where(col(Content.id).in_(ids))

    if owner_id is not None:
        statement = statement.where(col(Content.owner_id) == owner_id)

    deleted_ids = db.exec(statement.returning(col(Content.id))).all()

    if len(deleted_ids) != len(ids):
        db.rollback()

        raise ContentNotFoundError

    db.commit()


def list_admin_contents(
    *,
    request: AdminContentListRequest,
    db: Session,
) -> tuple[list[tuple[Content, User]], int]:
    owner_search = request.owner.strip()

    statement = select(Content, User).join(User)

    if owner_search:
        statement = statement.where(
            or_(
                col(User.name).icontains(owner_search, autoescape=True),
                col(User.email).icontains(owner_search, autoescape=True),
            )
        )

    return _paginate_contents(statement=statement, request=request, db=db)


def _paginate_contents[T](
    *,
    statement: SelectOfScalar[T] | Select[T],
    request: ContentListRequest,
    db: Session,
) -> tuple[list[T], int]:
    search = request.search.strip()

    if search:
        statement = statement.where(
            or_(
                col(Content.title).icontains(search, autoescape=True),
                col(Content.description).icontains(search, autoescape=True),
            )
        )

    if request.created_after is not None:
        statement = statement.where(col(Content.created_at) >= request.created_after)

    count = db.exec(select(func.count()).select_from(statement.subquery())).one()

    sort_column: Mapped[str] | Mapped[datetime]

    if request.sort == "title":
        sort_column = col(Content.title)
    else:
        sort_column = col(Content.created_at)

    if request.order == "asc":
        sort_order = sort_column.asc()
    else:
        sort_order = sort_column.desc()

    statement = statement.order_by(sort_order, col(Content.id))

    statement = statement.offset(request.skip).limit(request.limit)

    contents = list(db.exec(statement).all())

    return contents, count
