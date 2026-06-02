from fastapi import APIRouter, Depends, Query
from app.models.resource import ResourceCreate, ResourceUpdate, ResourceOut, ResourceStatusUpdate
from app.models.response import BaseResponse, PaginatedData, PaginatedResponse
from app.services import resource_service
from app.services.resource_service import _row_to_out
from app.utils.deps import get_current_user, get_admin_user
from app.config import DEFAULT_PAGE_SIZE
import aiosqlite
from app.database import get_db

router = APIRouter(prefix="/api/v1/resources", tags=["resources"])


@router.post("")
async def create_resource(data: ResourceCreate, current_user: dict = Depends(get_current_user)):
    r = await resource_service.create_resource(data, current_user["id"])
    return BaseResponse(data=r)


@router.get("")
async def list_resources(
    sort: str = Query("hot"),
    category_id: int | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=50),
):
    items, total = await resource_service.list_resources(sort, category_id, page, page_size)
    return PaginatedResponse(data=PaginatedData(items=items, total=total, page=page, page_size=page_size))


@router.get("/search")
async def search_resources(
    q: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=50),
):
    if not q.strip():
        items, total = [], 0
    else:
        items, total = await resource_service.search_resources(q, page, page_size)
    return PaginatedResponse(data=PaginatedData(items=items, total=total, page=page, page_size=page_size))


@router.get("/{resource_id}")
async def get_resource(resource_id: int):
    r = await resource_service.get_resource(resource_id)
    return BaseResponse(data=r)


@router.put("/{resource_id}")
async def update_resource(
    resource_id: int, data: ResourceUpdate,
    current_user: dict = Depends(get_current_user),
):
    r = await resource_service.update_resource(resource_id, data, current_user)
    return BaseResponse(data=r)


@router.delete("/{resource_id}")
async def delete_resource(resource_id: int, _admin=Depends(get_admin_user)):
    await resource_service.delete_resource(resource_id)
    return BaseResponse(data=None)


@router.post("/{resource_id}/favorite")
async def favorite_resource(resource_id: int, current_user: dict = Depends(get_current_user)):
    favorited = await resource_service.toggle_favorite(resource_id, current_user["id"])
    return BaseResponse(data={"favorited": favorited})


@router.delete("/{resource_id}/favorite")
async def unfavorite_resource(resource_id: int, current_user: dict = Depends(get_current_user)):
    favorited = await resource_service.toggle_favorite(resource_id, current_user["id"])
    return BaseResponse(data={"favorited": favorited})
