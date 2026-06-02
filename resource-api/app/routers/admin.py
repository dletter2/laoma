from fastapi import APIRouter, Depends, Query
from app.models.resource import ResourceStatusUpdate, UserStatusUpdate
from app.models.response import BaseResponse, PaginatedData, PaginatedResponse
from app.services import admin_service
from app.utils.deps import get_admin_user
from app.config import DEFAULT_PAGE_SIZE

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.put("/resources/{resource_id}/status")
async def update_resource_status(resource_id: int, data: ResourceStatusUpdate, _admin=Depends(get_admin_user)):
    await admin_service.update_resource_status(resource_id, data)
    return BaseResponse(data=None)


@router.get("/users")
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    _admin=Depends(get_admin_user),
):
    items, total = await admin_service.list_users(page, page_size)
    return PaginatedResponse(data=PaginatedData(items=items, total=total, page=page, page_size=page_size))


@router.put("/users/{user_id}/status")
async def update_user_status(user_id: int, data: UserStatusUpdate, _admin=Depends(get_admin_user)):
    await admin_service.update_user_status(user_id, data)
    return BaseResponse(data=None)


@router.get("/statistics")
async def get_statistics(_admin=Depends(get_admin_user)):
    stats = await admin_service.get_statistics()
    return BaseResponse(data=stats)
