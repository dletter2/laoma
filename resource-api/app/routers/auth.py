from fastapi import APIRouter, Depends
from app.models.user import UserRegister, UserLogin, UserOut, TokenResponse, RefreshRequest
from app.models.response import BaseResponse
from app.services import auth_service
from app.utils.deps import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register")
async def register(data: UserRegister):
    user = await auth_service.register(data)
    return BaseResponse(data=user)


@router.post("/login")
async def login(data: UserLogin):
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
