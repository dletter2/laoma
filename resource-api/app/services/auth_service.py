import aiosqlite
from passlib.context import CryptContext
from app.database import get_db
from app.middleware.error_handler import BadRequestException, UnauthorizedException
from app.models.user import UserRegister, UserLogin, UserOut, TokenResponse, RefreshRequest
from app.utils.jwt import create_access_token, create_refresh_token, decode_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


async def register(data: UserRegister) -> UserOut:
    if len(data.username) < 2:
        raise BadRequestException("用户名至少2个字符")
    if len(data.password) < 6:
        raise BadRequestException("密码至少6位")
    db = await get_db()
    cursor = await db.execute("SELECT id FROM users WHERE username = ?", (data.username,))
    if await cursor.fetchone():
        raise BadRequestException("用户名已存在")
    hashed = hash_password(data.password)
    cursor = await db.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (data.username, hashed),
    )
    await db.commit()
    return UserOut(id=cursor.lastrowid, username=data.username, role="user")


async def login(data: UserLogin) -> TokenResponse:
    db = await get_db()
    cursor = await db.execute(
        "SELECT id, username, role, password_hash, status FROM users WHERE username = ?",
        (data.username,),
    )
    user = await cursor.fetchone()
    if not user or not verify_password(data.password, user["password_hash"]):
        raise BadRequestException("用户名或密码错误")
    if user["status"] != "active":
        raise UnauthorizedException("账户已被禁用")
    access = create_access_token({"sub": str(user["id"]), "role": user["role"]})
    refresh = create_refresh_token({"sub": str(user["id"]), "role": user["role"]})
    return TokenResponse(access_token=access, refresh_token=refresh)


async def refresh_token(data: RefreshRequest) -> TokenResponse:
    payload = decode_token(data.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise UnauthorizedException("Refresh token无效或已过期")
    user_id = payload.get("sub")
    db = await get_db()
    cursor = await db.execute("SELECT id, role, status FROM users WHERE id = ?", (user_id,))
    user = await cursor.fetchone()
    if not user or user["status"] != "active":
        raise UnauthorizedException("用户不存在或已禁用")
    access = create_access_token({"sub": str(user["id"]), "role": user["role"]})
    refresh = create_refresh_token({"sub": str(user["id"]), "role": user["role"]})
    return TokenResponse(access_token=access, refresh_token=refresh)


async def get_me(user_id: int) -> UserOut:
    db = await get_db()
    cursor = await db.execute("SELECT id, username, role, created_at FROM users WHERE id = ?", (user_id,))
    user = await cursor.fetchone()
    if not user:
        raise UnauthorizedException("用户不存在")
    return UserOut(id=user["id"], username=user["username"], role=user["role"], created_at=user["created_at"])
