import aiosqlite
from datetime import datetime, timezone
from app.database import get_db
from app.middleware.error_handler import NotFoundException, BadRequestException
from app.models.resource import ResourceStatusUpdate, UserStatusUpdate


async def list_resources(
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
) -> tuple[list[dict], int]:
    db = await get_db()
    conditions: list[str] = []
    params: list = []
    if status:
        conditions.append("r.status = ?")
        params.append(status)
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    cursor = await db.execute(f"SELECT COUNT(*) as cnt FROM resources r {where}", params)
    total = (await cursor.fetchone())["cnt"]
    offset = (page - 1) * page_size
    cursor = await db.execute(
        f"""SELECT r.*, c.name as category_name, u.username as uploader_name, u.nickname as uploader_nickname
            FROM resources r
            LEFT JOIN categories c ON r.category_id = c.id
            LEFT JOIN users u ON r.uploader_id = u.id
            {where} ORDER BY r.upload_time DESC LIMIT ? OFFSET ?""",
        params + [page_size, offset],
    )
    rows = await cursor.fetchall()
    return [dict(r) for r in rows], total


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
        "SELECT id, username, nickname, role, status, created_at FROM users ORDER BY id DESC LIMIT ? OFFSET ?",
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


async def delete_resource(resource_id: int) -> None:
    db = await get_db()
    cursor = await db.execute("SELECT id FROM resources WHERE id = ?", (resource_id,))
    if not await cursor.fetchone():
        raise NotFoundException("资源不存在")
    await db.execute("DELETE FROM favorites WHERE resource_id = ?", (resource_id,))
    await db.execute("DELETE FROM resources WHERE id = ?", (resource_id,))
    await db.commit()


async def batch_update_status(ids: list[int], status: str) -> int:
    db = await get_db()
    valid = {"approved", "rejected", "published", "unpublished"}
    if status not in valid:
        raise BadRequestException(f"无效状态，可选: {', '.join(valid)}")
    if not ids:
        raise BadRequestException("ids不能为空")
    placeholders = ",".join("?" * len(ids))
    cursor = await db.execute(
        f"UPDATE resources SET status = ? WHERE id IN ({placeholders})",
        [status] + ids,
    )
    await db.commit()
    return cursor.rowcount


async def batch_delete(ids: list[int]) -> int:
    db = await get_db()
    if not ids:
        raise BadRequestException("ids不能为空")
    placeholders = ",".join("?" * len(ids))
    await db.execute(f"DELETE FROM favorites WHERE resource_id IN ({placeholders})", ids)
    cursor = await db.execute(f"DELETE FROM resources WHERE id IN ({placeholders})", ids)
    await db.commit()
    return cursor.rowcount


async def get_statistics() -> dict:
    db = await get_db()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM resources")
    resource_count = (await cursor.fetchone())["cnt"]
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM users")
    user_count = (await cursor.fetchone())["cnt"]
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM resources WHERE date(upload_time) = ?", (today,))
    today_resources = (await cursor.fetchone())["cnt"]
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM users WHERE date(created_at) = ?", (today,))
    today_users = (await cursor.fetchone())["cnt"]
    cursor = await db.execute("""
        SELECT status, COUNT(*) as cnt FROM resources GROUP BY status
    """)
    status_rows = await cursor.fetchall()
    status_counts = {r["status"]: r["cnt"] for r in status_rows}
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
        "pending_count": status_counts.get("pending", 0),
        "published_count": status_counts.get("published", 0),
        "status_counts": status_counts,
        "category_distribution": category_dist,
    }
