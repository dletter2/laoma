from fastapi import Depends, Request
from app.database import get_db
from app.middleware.error_handler import UnauthorizedException, ForbiddenException
from app.utils.jwt import decode_token
import aiosqlite


async def get_current_user(request: Request, db: aiosqlite.Connection = Depends(get_db)) -> dict:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise UnauthorizedException()
    token = auth_header[7:]
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise UnauthorizedException("Token无效或已过期")
    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException()
    cursor = await db.execute("SELECT id, username, role, status FROM users WHERE id = ?", (user_id,))
    user = await cursor.fetchone()
    if user is None:
        raise UnauthorizedException("用户不存在")
    if user["status"] != "active":
        raise UnauthorizedException("账户已被禁用")
    return {"id": user["id"], "username": user["username"], "role": user["role"]}


async def get_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] != "admin":
        raise ForbiddenException("需要管理员权限")
    return current_user
