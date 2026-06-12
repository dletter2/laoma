from fastapi import APIRouter
from app.models.response import BaseResponse
from app.services import share_service

router = APIRouter(prefix="/api/v1/shares", tags=["shares"])


@router.get("")
async def list_shares():
    items = await share_service.list_shares()
    return BaseResponse(data=items)
