import uuid

from sqlmodel import Session, col, func, select

from app.items.models import Item
from app.items.schemas import ItemCreate, ItemUpdate


def list_items(
    *, session: Session, owner_id: uuid.UUID | None, skip: int, limit: int
) -> tuple[list[Item], int]:
    count_statement = select(func.count()).select_from(Item)
    statement = select(Item)

    if owner_id is not None:
        count_statement = count_statement.where(Item.owner_id == owner_id)
        statement = statement.where(Item.owner_id == owner_id)

    count = session.exec(count_statement).one()

    items = session.exec(
        statement.order_by(col(Item.created_at).desc()).offset(skip).limit(limit)
    ).all()

    items = list(items)

    return items, count


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    item = Item.model_validate(item_in, update={"owner_id": owner_id})

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


def update_item(*, session: Session, item: Item, item_in: ItemUpdate) -> Item:
    item.sqlmodel_update(item_in.model_dump(exclude_unset=True))

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


def delete_item(*, session: Session, item: Item) -> None:
    session.delete(item)
    session.commit()
