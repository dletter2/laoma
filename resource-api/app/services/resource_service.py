import logging
import aiosqlite
from app.database import get_db
from app.config import DEFAULT_PAGE_SIZE
from app.middleware.error_handler import BadRequestException, NotFoundException, ForbiddenException
from app.models.resource import ResourceCreate, ResourceUpdate, ResourceOut


def _row_to_out(r: aiosqlite.Row) -> ResourceOut:
    keys = r.keys()
    return ResourceOut(
        id=r["id"], title=r["title"], summary=r["summary"],
        category_id=r["category_id"],
        category_name=r["category_name"] if "category_name" in keys else "",
        tags=r["tags"] or "", link=r["link"] or "",
        link_password=r["link_password"] or "",
        file_size=int(r["file_size"] or 0), upload_time=r["upload_time"],
        is_hot=r["is_hot"], view_count=r["view_count"],
        favorite_count=r["favorite_count"], uploader_id=r["uploader_id"],
        uploader_nickname=r["uploader_nickname"] if "uploader_nickname" in keys else "",
        status=r["status"],
    )


async def create_resource(data: ResourceCreate, uploader_id: int) -> ResourceOut:
    db = await get_db()
    cursor = await db.execute("SELECT id FROM categories WHERE id = ?", (data.category_id,))
    if not await cursor.fetchone():
        raise BadRequestException("分类不存在")
    cursor = await db.execute(
        """INSERT INTO resources (title, summary, category_id, tags, link, link_password, file_size, uploader_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (data.title, data.summary, data.category_id, data.tags,
         data.link, data.link_password, int(data.file_size), uploader_id),
    )
    await db.commit()
    cursor2 = await db.execute("SELECT nickname FROM users WHERE id = ?", (uploader_id,))
    user_row = await cursor2.fetchone()
    uploader_name = user_row["nickname"] or str(uploader_id) if user_row else str(uploader_id)
    from app.services.notification_service import notify_new_resource
    import asyncio

    def _log_notify_error(task: asyncio.Task):
        if task.exception():
            logging.getLogger(__name__).warning("钉钉通知发送失败: %s", task.exception())

    task = asyncio.create_task(notify_new_resource(data.title, data.summary, uploader_name))
    task.add_done_callback(_log_notify_error)
    return await get_resource(cursor.lastrowid, increment_view=False)


async def list_resources(
    sort: str = "hot",
    category_id: int | None = None,
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> tuple[list[ResourceOut], int]:
    db = await get_db()
    conditions = ["r.status = 'published'"]
    params: list = []
    if category_id:
        conditions.append("r.category_id = ?")
        params.append(category_id)
    where = " AND ".join(conditions)
    order = "r.view_count + r.favorite_count DESC, r.upload_time DESC" if sort == "hot" else "r.upload_time DESC"
    # count
    cursor = await db.execute(f"SELECT COUNT(*) as cnt FROM resources r WHERE {where}", params)
    total = (await cursor.fetchone())["cnt"]
    # data
    offset = (page - 1) * page_size
    cursor = await db.execute(
        f"""SELECT r.*, c.name as category_name, u.nickname as uploader_nickname FROM resources r
            LEFT JOIN categories c ON r.category_id = c.id
            LEFT JOIN users u ON r.uploader_id = u.id
            WHERE {where} ORDER BY {order} LIMIT ? OFFSET ?""",
        params + [page_size, offset],
    )
    rows = await cursor.fetchall()
    return [_row_to_out(r) for r in rows], total


async def search_resources(q: str, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE) -> tuple[list[ResourceOut], int]:
    db = await get_db()
    like = f"%{q}%"
    where = """r.status = 'published' AND (
        r.title LIKE ? OR r.summary LIKE ? OR r.tags LIKE ? OR c.name LIKE ?
    )"""
    params = [like, like, like, like]
    join = "LEFT JOIN categories c ON r.category_id = c.id LEFT JOIN users u ON r.uploader_id = u.id"
    cursor = await db.execute(f"SELECT COUNT(*) as cnt FROM resources r {join} WHERE {where}", params)
    total = (await cursor.fetchone())["cnt"]
    offset = (page - 1) * page_size
    cursor = await db.execute(
        f"""SELECT r.*, c.name as category_name, u.nickname as uploader_nickname FROM resources r
            {join}
            WHERE {where} ORDER BY r.upload_time DESC LIMIT ? OFFSET ?""",
        params + [page_size, offset],
    )
    rows = await cursor.fetchall()
    return [_row_to_out(r) for r in rows], total


async def get_resource(resource_id: int, increment_view: bool = True) -> ResourceOut:
    db = await get_db()
    if increment_view:
        await db.execute("UPDATE resources SET view_count = view_count + 1 WHERE id = ?", (resource_id,))
        await db.commit()
    cursor = await db.execute(
        """SELECT r.*, c.name as category_name, u.nickname as uploader_nickname FROM resources r
           LEFT JOIN categories c ON r.category_id = c.id
           LEFT JOIN users u ON r.uploader_id = u.id WHERE r.id = ?""",
        (resource_id,),
    )
    row = await cursor.fetchone()
    if not row:
        raise NotFoundException("资源不存在")
    return _row_to_out(row)


async def update_resource(resource_id: int, data: ResourceUpdate, user: dict) -> ResourceOut:
    db = await get_db()
    cursor = await db.execute("SELECT * FROM resources WHERE id = ?", (resource_id,))
    row = await cursor.fetchone()
    if not row:
        raise NotFoundException("资源不存在")
    if row["uploader_id"] != user["id"] and user["role"] != "admin":
        raise ForbiddenException("无权修改此资源")
    updates = []
    params = []
    for field, value in data.model_dump(exclude_unset=True).items():
        updates.append(f"{field} = ?")
        if field == "file_size" and value is not None:
            params.append(int(value))
        else:
            params.append(value)
    if not updates:
        return _row_to_out(row)
    params.append(resource_id)
    await db.execute(f"UPDATE resources SET {', '.join(updates)} WHERE id = ?", params)
    await db.commit()
    return await get_resource(resource_id, increment_view=False)


async def delete_resource(resource_id: int) -> None:
    db = await get_db()
    cursor = await db.execute("SELECT id FROM resources WHERE id = ?", (resource_id,))
    if not await cursor.fetchone():
        raise NotFoundException("资源不存在")
    await db.execute("DELETE FROM favorites WHERE resource_id = ?", (resource_id,))
    await db.execute("DELETE FROM resources WHERE id = ?", (resource_id,))
    await db.commit()


async def toggle_favorite(resource_id: int, user_id: int) -> bool:
    """Returns True if favorited, False if unfavorited."""
    db = await get_db()
    cursor = await db.execute("SELECT id FROM resources WHERE id = ? AND status = 'published'", (resource_id,))
    if not await cursor.fetchone():
        raise NotFoundException("资源不存在")
    cursor = await db.execute("SELECT id FROM favorites WHERE user_id = ? AND resource_id = ?", (user_id, resource_id))
    existing = await cursor.fetchone()
    if existing:
        await db.execute("DELETE FROM favorites WHERE user_id = ? AND resource_id = ?", (user_id, resource_id))
        await db.execute("UPDATE resources SET favorite_count = favorite_count - 1 WHERE id = ?", (resource_id,))
        await db.commit()
        return False
    else:
        await db.execute("INSERT INTO favorites (user_id, resource_id) VALUES (?, ?)", (user_id, resource_id))
        await db.execute("UPDATE resources SET favorite_count = favorite_count + 1 WHERE id = ?", (resource_id,))
        await db.commit()
        return True


async def list_my_resources(user_id: int, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE) -> tuple[list[ResourceOut], int]:
    db = await get_db()
    cursor = await db.execute(
        "SELECT COUNT(*) as cnt FROM resources WHERE uploader_id = ?", (user_id,),
    )
    total = (await cursor.fetchone())["cnt"]
    offset = (page - 1) * page_size
    cursor = await db.execute(
        """SELECT r.*, c.name as category_name, u.nickname as uploader_nickname FROM resources r
           LEFT JOIN categories c ON r.category_id = c.id
           LEFT JOIN users u ON r.uploader_id = u.id
           WHERE r.uploader_id = ?
           ORDER BY r.upload_time DESC LIMIT ? OFFSET ?""",
        (user_id, page_size, offset),
    )
    rows = await cursor.fetchall()
    return [_row_to_out(r) for r in rows], total


async def list_favorites(user_id: int, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE) -> tuple[list[ResourceOut], int]:
    db = await get_db()
    cursor = await db.execute(
        "SELECT COUNT(*) as cnt FROM favorites f JOIN resources r ON f.resource_id = r.id WHERE f.user_id = ? AND r.status = 'published'",
        (user_id,),
    )
    total = (await cursor.fetchone())["cnt"]
    offset = (page - 1) * page_size
    cursor = await db.execute(
        """SELECT r.*, c.name as category_name, u.nickname as uploader_nickname FROM favorites f
           JOIN resources r ON f.resource_id = r.id
           LEFT JOIN categories c ON r.category_id = c.id
           LEFT JOIN users u ON r.uploader_id = u.id
           WHERE f.user_id = ? AND r.status = 'published'
           ORDER BY f.created_at DESC LIMIT ? OFFSET ?""",
        (user_id, page_size, offset),
    )
    rows = await cursor.fetchall()
    return [_row_to_out(r) for r in rows], total
