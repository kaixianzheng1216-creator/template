import uuid
from typing import Annotated

from fastapi import APIRouter, Query, status

from app.auth.dependencies import CurrentAdmin, CurrentUser
from app.contents import service
from app.contents.schemas import (
    AdminContentListRequest,
    AdminContentListResponse,
    AdminContentResponse,
    ContentBatchDeleteRequest,
    ContentCreateRequest,
    ContentListRequest,
    ContentListResponse,
    ContentResponse,
    ContentUpdateRequest,
)
from app.database import DbDep

router = APIRouter(prefix="/contents", tags=["contents"])
admin_router = APIRouter(prefix="/admin/contents", tags=["admin-contents"])


@router.get(
    "",
    summary="分页查询我的内容",
)
def list_contents(
    request: Annotated[ContentListRequest, Query()],
    current_user: CurrentUser,
    db: DbDep,
) -> ContentListResponse:
    contents, count = service.list_contents(
        request=request,
        owner_id=current_user.id,
        db=db,
    )

    return ContentListResponse.model_validate({"data": contents, "count": count})


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="创建内容",
)
def create_content(
    request: ContentCreateRequest,
    current_user: CurrentUser,
    db: DbDep,
) -> ContentResponse:
    content = service.create_content(
        request=request,
        owner_id=current_user.id,
        db=db,
    )

    return ContentResponse.model_validate(content)


@router.put(
    "/{content_id}",
    summary="更新我的内容",
)
def update_content(
    content_id: uuid.UUID,
    request: ContentUpdateRequest,
    current_user: CurrentUser,
    db: DbDep,
) -> ContentResponse:
    content = service.update_content(
        content_id=content_id,
        request=request,
        owner_id=current_user.id,
        db=db,
    )

    return ContentResponse.model_validate(content)


@router.post(
    "/bulk-delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="批量删除我的内容",
)
def delete_contents(
    request: ContentBatchDeleteRequest,
    current_user: CurrentUser,
    db: DbDep,
) -> None:
    service.delete_contents(
        content_ids=request.ids,
        owner_id=current_user.id,
        db=db,
    )


@admin_router.get(
    "",
    summary="分页查询所有用户的内容",
)
def list_all_contents(
    request: Annotated[AdminContentListRequest, Query()],
    _current_admin: CurrentAdmin,
    db: DbDep,
) -> AdminContentListResponse:
    content_owners, count = service.list_admin_contents(
        request=request,
        db=db,
    )

    data: list[AdminContentResponse] = []

    for content, owner in content_owners:
        data.append(
            AdminContentResponse.model_validate(content, update={"owner": owner})
        )

    return AdminContentListResponse(data=data, count=count)


@admin_router.put(
    "/{content_id}",
    summary="更新用户内容",
)
def update_any_content(
    content_id: uuid.UUID,
    request: ContentUpdateRequest,
    _current_admin: CurrentAdmin,
    db: DbDep,
) -> ContentResponse:
    content = service.update_content(
        content_id=content_id,
        request=request,
        owner_id=None,
        db=db,
    )

    return ContentResponse.model_validate(content)


@admin_router.post(
    "/bulk-delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="批量删除用户内容",
)
def delete_any_contents(
    request: ContentBatchDeleteRequest,
    _current_admin: CurrentAdmin,
    db: DbDep,
) -> None:
    service.delete_contents(
        content_ids=request.ids,
        owner_id=None,
        db=db,
    )
