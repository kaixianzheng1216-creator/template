import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app.auth.dependencies import CurrentUser, SessionDep
from app.items import service
from app.items.models import Item
from app.items.schemas import ItemCreate, ItemPublic, ItemsPublic, ItemUpdate
from app.schemas import Message

router = APIRouter(prefix="/items", tags=["items"])


def _get_accessible_item(
    *, session: SessionDep, current_user: CurrentUser, item_id: uuid.UUID
) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return item


@router.get("/", response_model=ItemsPublic)
def read_items(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    owner_id = None if current_user.is_superuser else current_user.id
    items, count = service.list_items(
        session=session,
        owner_id=owner_id,
        skip=skip,
        limit=limit,
    )
    return ItemsPublic(
        data=[ItemPublic.model_validate(item) for item in items],
        count=count,
    )


@router.get("/{id}", response_model=ItemPublic)
def read_item(
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
) -> Any:
    return _get_accessible_item(
        session=session,
        current_user=current_user,
        item_id=id,
    )


@router.post("/", response_model=ItemPublic)
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
    return service.create_item(
        session=session,
        item_in=item_in,
        owner_id=current_user.id,
    )


@router.put("/{id}", response_model=ItemPublic)
def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    item_in: ItemUpdate,
) -> Any:
    item = _get_accessible_item(
        session=session,
        current_user=current_user,
        item_id=id,
    )
    return service.update_item(session=session, item=item, item_in=item_in)


@router.delete("/{id}")
def delete_item(
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
) -> Message:
    item = _get_accessible_item(
        session=session,
        current_user=current_user,
        item_id=id,
    )
    service.delete_item(session=session, item=item)
    return Message(message="Item deleted successfully")
