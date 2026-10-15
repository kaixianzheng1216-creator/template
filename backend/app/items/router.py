import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Path, Query, status

from app.auth.dependencies import CurrentUser, SessionDep
from app.items import service
from app.items.schemas import (
    ItemCreate,
    ItemPublic,
    ItemsPublic,
    ItemUpdate,
)
from app.schemas import PaginationRequest

router = APIRouter(prefix="/items", tags=["items"])


@router.get(
    "",
    summary="分页获取条目列表",
)
def read_items(
    session: SessionDep,
    current_user: CurrentUser,
    pagination: Annotated[PaginationRequest, Query()],
) -> ItemsPublic:
    items, count = service.list_items(
        session=session,
        current_user=current_user,
        skip=pagination.skip,
        limit=pagination.limit,
    )

    response = ItemsPublic(
        data=[ItemPublic.model_validate(item) for item in items],
        count=count,
    )

    return response


@router.post(
    "",
    summary="创建条目",
)
def create_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    item_in: Annotated[ItemCreate, Body(description="新条目信息")],
) -> ItemPublic:
    item = service.create_item(
        session=session,
        current_user=current_user,
        item_in=item_in,
    )

    response = ItemPublic.model_validate(item)

    return response


@router.get(
    "/{item_id}",
    summary="获取指定条目",
)
def read_item(
    session: SessionDep,
    current_user: CurrentUser,
    item_id: Annotated[uuid.UUID, Path(description="条目 ID")],
) -> ItemPublic:
    item = service.get_item(
        session=session,
        current_user=current_user,
        item_id=item_id,
    )

    response = ItemPublic.model_validate(item)

    return response


@router.patch(
    "/{item_id}",
    summary="更新指定条目",
)
def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    item_id: Annotated[uuid.UUID, Path(description="条目 ID")],
    item_in: Annotated[ItemUpdate, Body(description="条目更新信息")],
) -> ItemPublic:
    item = service.update_item(
        session=session,
        current_user=current_user,
        item_id=item_id,
        item_in=item_in,
    )

    response = ItemPublic.model_validate(item)

    return response


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除指定条目",
)
def delete_item(
    session: SessionDep,
    current_user: CurrentUser,
    item_id: Annotated[uuid.UUID, Path(description="条目 ID")],
) -> None:
    service.delete_item(
        session=session,
        current_user=current_user,
        item_id=item_id,
    )
