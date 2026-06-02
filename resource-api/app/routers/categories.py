from fastapi import APIRouter, Depends
from app.models.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.models.response import BaseResponse
from app.services import category_service
from app.utils.deps import get_admin_user

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


@router.get("")
async def list_categories():
    cats = await category_service.list_categories()
    return BaseResponse(data=cats)


@router.post("")
async def create_category(data: CategoryCreate, _admin=Depends(get_admin_user)):
    cat = await category_service.create_category(data)
    return BaseResponse(data=cat)


@router.put("/{cat_id}")
async def update_category(cat_id: int, data: CategoryUpdate, _admin=Depends(get_admin_user)):
    cat = await category_service.update_category(cat_id, data)
    return BaseResponse(data=cat)


@router.delete("/{cat_id}")
async def delete_category(cat_id: int, _admin=Depends(get_admin_user)):
    await category_service.delete_category(cat_id)
    return BaseResponse(data=None)
