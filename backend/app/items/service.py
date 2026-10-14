import uuid

from sqlmodel import Session, col, func, select

from app.items.exceptions import ItemAccessDeniedError, ItemNotFoundError
from app.items.models import Item
from app.items.schemas import ItemCreate, ItemUpdate
from app.users.models import User


def list_items(
    *,
    session: Session,
    current_user: User,
    skip: int,
    limit: int,
) -> tuple[list[Item], int]:
    statement = select(Item)
    count_statement = select(func.count()).select_from(Item)

    if not current_user.is_superuser:
        statement = statement.where(Item.owner_id == current_user.id)
        count_statement = count_statement.where(Item.owner_id == current_user.id)

    items = list(
        session.exec(
            statement.order_by(col(Item.created_at).desc()).offset(skip).limit(limit)
        ).all()
    )

    count = session.exec(count_statement).one()

    return items, count


def create_item(
    *,
    session: Session,
    current_user: User,
    item_in: ItemCreate,
) -> Item:
    item = Item.model_validate(item_in, update={"owner_id": current_user.id})

    session.add(item)

    session.commit()

    session.refresh(item)

    return item


def get_item(
    *,
    session: Session,
    current_user: User,
    item_id: uuid.UUID,
) -> Item:
    item = session.get(Item, item_id)

    if item is None:
        raise ItemNotFoundError

    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise ItemAccessDeniedError

    return item


def update_item(
    *,
    session: Session,
    current_user: User,
    item_id: uuid.UUID,
    item_in: ItemUpdate,
) -> Item:
    item = get_item(
        session=session,
        current_user=current_user,
        item_id=item_id,
    )

    item.sqlmodel_update(item_in.model_dump(exclude_unset=True))

    session.add(item)

    session.commit()

    session.refresh(item)

    return item


def delete_item(
    *,
    session: Session,
    current_user: User,
    item_id: uuid.UUID,
) -> None:
    item = get_item(
        session=session,
        current_user=current_user,
        item_id=item_id,
    )

    session.delete(item)

    session.commit()
