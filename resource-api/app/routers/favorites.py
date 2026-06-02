from fastapi import APIRouter, Depends, Query
from app.models.response import BaseResponse, PaginatedData, PaginatedResponse
from app.services import resource_service
from app.utils.deps import get_current_user
from app.config import DEFAULT_PAGE_SIZE

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/me/favorites")
async def list_my_favorites(
    current_user: dict = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=50),
):
    items, total = await resource_service.list_favorites(current_user["id"], page, page_size)
    return PaginatedResponse(data=PaginatedData(items=items, total=total, page=page, page_size=page_size))
