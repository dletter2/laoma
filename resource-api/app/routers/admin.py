from fastapi import APIRouter, Depends, Query
from app.models.resource import ResourceStatusUpdate, UserStatusUpdate, BatchStatusUpdate, BatchDelete
from app.models.share import ShareCreate, ShareUpdate
from app.models.response import BaseResponse, PaginatedData, PaginatedResponse
from app.services import admin_service, share_service
from app.services.notification_service import get_setting, set_setting
from app.utils.deps import get_admin_user
from app.config import DEFAULT_PAGE_SIZE
from app.middleware.error_handler import BadRequestException

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/resources")
async def list_resources(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    status: str | None = Query(None),
    _admin=Depends(get_admin_user),
):
    items, total = await admin_service.list_resources(page, page_size, status)
    return PaginatedResponse(data=PaginatedData(items=items, total=total, page=page, page_size=page_size))


@router.put("/resources/batch/status")
async def batch_update_status(data: BatchStatusUpdate, _admin=Depends(get_admin_user)):
    count = await admin_service.batch_update_status(data.ids, data.status)
    return BaseResponse(data={"affected": count})


@router.post("/resources/batch/delete")
async def batch_delete(data: BatchDelete, _admin=Depends(get_admin_user)):
    count = await admin_service.batch_delete(data.ids)
    return BaseResponse(data={"affected": count})


@router.put("/resources/{resource_id}/status")
async def update_resource_status(resource_id: int, data: ResourceStatusUpdate, _admin=Depends(get_admin_user)):
    await admin_service.update_resource_status(resource_id, data)
    return BaseResponse(data=None)


@router.delete("/resources/{resource_id}")
async def delete_resource(resource_id: int, _admin=Depends(get_admin_user)):
    await admin_service.delete_resource(resource_id)
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


# ===== Share Resource Management =====

@router.post("/shares")
async def create_share(data: ShareCreate, _admin=Depends(get_admin_user)):
    r = await share_service.create_share(data)
    return BaseResponse(data=r)


@router.get("/shares")
async def list_shares(_admin=Depends(get_admin_user)):
    items = await share_service.list_shares()
    return BaseResponse(data=items)


@router.put("/shares/{share_id}")
async def update_share(share_id: int, data: ShareUpdate, _admin=Depends(get_admin_user)):
    r = await share_service.update_share(share_id, data)
    return BaseResponse(data=r)


@router.delete("/shares/{share_id}")
async def delete_share(share_id: int, _admin=Depends(get_admin_user)):
    await share_service.delete_share(share_id)
    return BaseResponse(data=None)


@router.get("/settings/{key}")
async def get_settings_key(key: str, _admin=Depends(get_admin_user)):
    value = await get_setting(key)
    return BaseResponse(data={"key": key, "value": value or ""})


@router.put("/settings/{key}")
async def update_settings_key(key: str, value: str = Query(...), _admin=Depends(get_admin_user)):
    await set_setting(key, value)
    return BaseResponse(data=None)


@router.post("/settings/test-webhook")
async def test_webhook(_admin=Depends(get_admin_user)):
    webhook_url = await get_setting("dingtalk_webhook")
    if not webhook_url:
        raise BadRequestException("请先保存 Webhook 地址")
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(webhook_url, json={
                "msgtype": "text",
                "text": {"content": "【测试通知】钉钉 Webhook 配置成功！"},
            })
            result = resp.json()
            if result.get("errcode") != 0:
                raise BadRequestException(f"钉钉返回错误: {result.get('errmsg', '未知错误')}")
    except httpx.RequestError as e:
        raise BadRequestException(f"发送失败: {e}")
    return BaseResponse(data=None)
