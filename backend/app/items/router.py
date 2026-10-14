import uuid

from fastapi import APIRouter

from app.auth.dependencies import CurrentUser, SessionDep
from app.items import service
from app.items.constants import ItemMessage
from app.items.models import Item
from app.items.schemas import ItemCreate, ItemPublic, ItemsPublic, ItemUpdate
from app.schemas import Message

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemsPublic)
def read_items(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> ItemsPublic:
    items, count = service.list_items(
        session=session,
        current_user=current_user,
        skip=skip,
        limit=limit,
    )

    response = ItemsPublic(
        data=[ItemPublic.model_validate(item) for item in items],
        count=count,
    )

    return response


@router.get("/{id}", response_model=ItemPublic)
def read_item(
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
) -> Item:
    item = service.get_item(
        session=session,
        current_user=current_user,
        item_id=id,
    )

    return item


@router.post("/", response_model=ItemPublic)
def create_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    item_in: ItemCreate,
) -> Item:
    item = service.create_item(
        session=session,
        current_user=current_user,
        item_in=item_in,
    )

    return item


@router.put("/{id}", response_model=ItemPublic)
def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    item_in: ItemUpdate,
) -> Item:
    item = service.update_item(
        session=session,
        current_user=current_user,
        item_id=id,
        item_in=item_in,
    )

    return item


@router.delete("/{id}")
def delete_item(
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
) -> Message:
    service.delete_item(
        session=session,
        current_user=current_user,
        item_id=id,
    )

    response = Message(message=ItemMessage.ITEM_DELETED)

    return response
