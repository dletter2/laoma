from fastapi import APIRouter, Depends
from app.models.user import UserRegister, UserLogin, UserOut, TokenResponse, RefreshRequest, ChangePassword
from app.models.response import BaseResponse
from app.services import auth_service
from app.services.captcha_service import create_captcha, verify_captcha
from app.middleware.error_handler import BadRequestException
from app.utils.deps import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.get("/captcha")
async def captcha():
    data = create_captcha()
    return BaseResponse(data=data)


@router.post("/register")
async def register(data: UserRegister):
    if data.captcha_key or data.captcha_code:
        if not verify_captcha(data.captcha_key, data.captcha_code):
            raise BadRequestException("验证码错误")
    user = await auth_service.register(data)
    return BaseResponse(data=user)


@router.post("/login")
async def login(data: UserLogin):
    if data.captcha_key or data.captcha_code:
        if not verify_captcha(data.captcha_key, data.captcha_code):
            raise BadRequestException("验证码错误")
    tokens = await auth_service.login(data)
    return BaseResponse(data=tokens)


@router.post("/refresh")
async def refresh(data: RefreshRequest):
    tokens = await auth_service.refresh_token(data)
    return BaseResponse(data=tokens)


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    user = await auth_service.get_me(current_user["id"])
    return BaseResponse(data=user)


@router.put("/password")
async def change_password(data: ChangePassword, current_user: dict = Depends(get_current_user)):
    await auth_service.change_password(current_user["id"], data)
    return BaseResponse(data=None)
