import uuid

from sqlmodel import Session, col, func, select

from app.auth.service import AuthenticatedUser
from app.contents.exceptions import ContentNotFoundError
from app.contents.models import Content
from app.contents.schemas import ContentCreate, ContentListQuery, ContentUpdate


def list_contents(
    *,
    session: Session,
    current_user: AuthenticatedUser,
    content_query: ContentListQuery,
) -> tuple[list[Content], int]:
    statement = select(Content).where(Content.owner_id == current_user.user_id)

    title = content_query.title.strip()

    if title:
        statement = statement.where(
            col(Content.title).icontains(title, autoescape=True)
        )

    description = content_query.description.strip()

    if description:
        statement = statement.where(
            col(Content.description).icontains(description, autoescape=True)
        )

    if content_query.created_after is not None:
        statement = statement.where(
            col(Content.created_at) >= content_query.created_after
        )

    count_statement = select(func.count()).select_from(statement.subquery())

    total = session.exec(count_statement).one()

    if content_query.sort == "title":
        if content_query.order == "asc":
            statement = statement.order_by(col(Content.title).asc(), col(Content.id))
        else:
            statement = statement.order_by(col(Content.title).desc(), col(Content.id))
    elif content_query.order == "asc":
        statement = statement.order_by(col(Content.created_at).asc(), col(Content.id))
    else:
        statement = statement.order_by(col(Content.created_at).desc(), col(Content.id))

    statement = statement.offset(content_query.skip).limit(content_query.limit)

    contents = list(session.exec(statement).all())

    return contents, total


def create_content(
    *,
    session: Session,
    current_user: AuthenticatedUser,
    content_create: ContentCreate,
) -> Content:
    content = Content.model_validate(
        content_create,
        update={"owner_id": current_user.user_id},
    )

    session.add(content)
    session.commit()
    session.refresh(content)

    return content


def get_content(
    *,
    session: Session,
    current_user: AuthenticatedUser,
    content_id: uuid.UUID,
) -> Content:
    statement = select(Content).where(
        Content.id == content_id,
        Content.owner_id == current_user.user_id,
    )

    content = session.exec(statement).one_or_none()

    if content is None:
        raise ContentNotFoundError

    return content


def update_content(
    *,
    session: Session,
    current_user: AuthenticatedUser,
    content_id: uuid.UUID,
    content_update: ContentUpdate,
) -> Content:
    content = get_content(
        session=session,
        current_user=current_user,
        content_id=content_id,
    )

    content.sqlmodel_update(content_update.model_dump())

    session.commit()
    session.refresh(content)

    return content


def delete_contents(
    *,
    session: Session,
    current_user: AuthenticatedUser,
    content_ids: list[uuid.UUID],
) -> None:
    ids = set(content_ids)

    statement = select(Content).where(
        col(Content.id).in_(ids),
        Content.owner_id == current_user.user_id,
    )

    contents = session.exec(statement.order_by(col(Content.id)).with_for_update()).all()

    if len(contents) != len(ids):
        raise ContentNotFoundError

    for content in contents:
        session.delete(content)

    session.commit()
