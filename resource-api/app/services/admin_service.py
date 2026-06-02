import aiosqlite
from datetime import datetime, timezone
from app.database import get_db
from app.middleware.error_handler import NotFoundException, BadRequestException
from app.models.resource import ResourceStatusUpdate, UserStatusUpdate


async def update_resource_status(resource_id: int, data: ResourceStatusUpdate) -> None:
    db = await get_db()
    cursor = await db.execute("SELECT id FROM resources WHERE id = ?", (resource_id,))
    if not await cursor.fetchone():
        raise NotFoundException("资源不存在")
    valid = {"approved", "rejected", "published", "unpublished"}
    if data.status not in valid:
        raise BadRequestException(f"无效状态，可选: {', '.join(valid)}")
    await db.execute("UPDATE resources SET status = ? WHERE id = ?", (data.status, resource_id))
    await db.commit()


async def list_users(page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
    db = await get_db()
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM users")
    total = (await cursor.fetchone())["cnt"]
    offset = (page - 1) * page_size
    cursor = await db.execute(
        "SELECT id, username, role, status, created_at FROM users ORDER BY id DESC LIMIT ? OFFSET ?",
        (page_size, offset),
    )
    rows = await cursor.fetchall()
    return [dict(r) for r in rows], total


async def update_user_status(user_id: int, data: UserStatusUpdate) -> None:
    db = await get_db()
    cursor = await db.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not await cursor.fetchone():
        raise NotFoundException("用户不存在")
    if data.status not in ("active", "disabled"):
        raise BadRequestException("无效状态，可选: active, disabled")
    await db.execute("UPDATE users SET status = ? WHERE id = ?", (data.status, user_id))
    await db.commit()


async def get_statistics() -> dict:
    db = await get_db()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM resources")
    resource_count = (await cursor.fetchone())["cnt"]
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM users")
    user_count = (await cursor.fetchone())["cnt"]
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM resources WHERE date(upload_time) = ?", (today,))
    today_resources = (await cursor.fetchone())["cnt"]
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM users WHERE date(created_at) = ?", (today,))
    today_users = (await cursor.fetchone())["cnt"]
    cursor = await db.execute("""
        SELECT c.id, c.name, COUNT(r.id) as count
        FROM categories c LEFT JOIN resources r ON c.id = r.category_id AND r.status = 'published'
        GROUP BY c.id ORDER BY c.sort_order
    """)
    category_dist = [dict(r) for r in await cursor.fetchall()]
    return {
        "resource_count": resource_count,
        "user_count": user_count,
        "today_resources": today_resources,
        "today_users": today_users,
        "category_distribution": category_dist,
    }
