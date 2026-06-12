import aiosqlite
from app.database import get_db
from app.middleware.error_handler import NotFoundException
from app.models.share import ShareCreate, ShareUpdate, ShareOut


def _row_to_out(r: aiosqlite.Row) -> ShareOut:
    return ShareOut(
        id=r["id"], name=r["name"], url=r["url"],
        avatar_url=r["avatar_url"] or "", description=r["description"] or "",
        sort_order=r["sort_order"], created_at=r["created_at"],
        updated_at=r["updated_at"],
    )


async def create_share(data: ShareCreate) -> ShareOut:
    db = await get_db()
    await db.execute(
        """INSERT INTO shares (name, url, avatar_url, description, sort_order)
           VALUES (?, ?, ?, ?, ?)""",
        (data.name, data.url, data.avatar_url, data.description, data.sort_order),
    )
    await db.commit()
    cursor = await db.execute("SELECT * FROM shares ORDER BY id DESC LIMIT 1")
    row = await cursor.fetchone()
    return _row_to_out(row)


async def list_shares() -> list[ShareOut]:
    db = await get_db()
    cursor = await db.execute("SELECT * FROM shares ORDER BY sort_order ASC, id ASC")
    rows = await cursor.fetchall()
    return [_row_to_out(r) for r in rows]


async def get_share(share_id: int) -> ShareOut:
    db = await get_db()
    cursor = await db.execute("SELECT * FROM shares WHERE id = ?", (share_id,))
    row = await cursor.fetchone()
    if not row:
        raise NotFoundException("分享资源不存在")
    return _row_to_out(row)


async def update_share(share_id: int, data: ShareUpdate) -> ShareOut:
    db = await get_db()
    cursor = await db.execute("SELECT * FROM shares WHERE id = ?", (share_id,))
    if not await cursor.fetchone():
        raise NotFoundException("分享资源不存在")
    updates = []
    params = []
    for field, value in data.model_dump(exclude_unset=True).items():
        updates.append(f"{field} = ?")
        params.append(value)
    if not updates:
        return await get_share(share_id)
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(share_id)
    await db.execute(f"UPDATE shares SET {', '.join(updates)} WHERE id = ?", params)
    await db.commit()
    return await get_share(share_id)


async def delete_share(share_id: int) -> None:
    db = await get_db()
    cursor = await db.execute("SELECT id FROM shares WHERE id = ?", (share_id,))
    if not await cursor.fetchone():
        raise NotFoundException("分享资源不存在")
    await db.execute("DELETE FROM shares WHERE id = ?", (share_id,))
    await db.commit()
