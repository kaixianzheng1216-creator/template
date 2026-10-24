import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Path, Query, status

from app.auth.dependencies import CurrentUser
from app.contents import service
from app.contents.schemas import (
    ContentBatchDelete,
    ContentCreate,
    ContentListQuery,
    ContentPublic,
    ContentsPublic,
    ContentUpdate,
)
from app.database import SessionDep

router = APIRouter(prefix="/contents", tags=["contents"])


@router.get(
    "",
    summary="分页获取内容列表",
)
def list_contents(
    session: SessionDep,
    current_user: CurrentUser,
    content_query: Annotated[ContentListQuery, Query()],
) -> ContentsPublic:
    contents, total = service.list_contents(
        session=session,
        current_user=current_user,
        content_query=content_query,
    )

    data: list[ContentPublic] = []

    for content in contents:
        data.append(ContentPublic.model_validate(content))

    return ContentsPublic(data=data, count=total)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="创建内容",
)
def create_content(
    session: SessionDep,
    current_user: CurrentUser,
    content_create: Annotated[ContentCreate, Body(description="新内容信息")],
) -> ContentPublic:
    content = service.create_content(
        session=session,
        current_user=current_user,
        content_create=content_create,
    )

    return ContentPublic.model_validate(content)


@router.put(
    "/{content_id}",
    summary="更新指定内容",
)
def update_content(
    session: SessionDep,
    current_user: CurrentUser,
    content_id: Annotated[uuid.UUID, Path(description="内容 ID")],
    content_update: Annotated[ContentUpdate, Body(description="内容更新信息")],
) -> ContentPublic:
    content = service.update_content(
        session=session,
        current_user=current_user,
        content_id=content_id,
        content_update=content_update,
    )

    return ContentPublic.model_validate(content)


@router.post(
    "/bulk-delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="批量删除内容",
)
def delete_contents(
    session: SessionDep,
    current_user: CurrentUser,
    content_batch_delete: Annotated[
        ContentBatchDelete, Body(description="待删除的内容")
    ],
) -> None:
    service.delete_contents(
        session=session,
        current_user=current_user,
        content_ids=content_batch_delete.ids,
    )
