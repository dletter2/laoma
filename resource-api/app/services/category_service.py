import aiosqlite
from app.database import get_db
from app.middleware.error_handler import BadRequestException, NotFoundException
from app.models.category import CategoryCreate, CategoryUpdate, CategoryOut


async def list_categories() -> list[CategoryOut]:
    db = await get_db()
    cursor = await db.execute("""
        SELECT c.id, c.name, c.sort_order, c.created_at,
               (SELECT COUNT(*) FROM resources WHERE category_id = c.id AND status = 'published') as resource_count
        FROM categories c
        ORDER BY c.sort_order ASC
    """)
    rows = await cursor.fetchall()
    return [
        CategoryOut(
            id=r["id"], name=r["name"], sort_order=r["sort_order"],
            resource_count=r["resource_count"], created_at=r["created_at"],
        )
        for r in rows
    ]


async def create_category(data: CategoryCreate) -> CategoryOut:
    db = await get_db()
    try:
        cursor = await db.execute(
            "INSERT INTO categories (name, sort_order) VALUES (?, ?)",
            (data.name, data.sort_order),
        )
        await db.commit()
    except aiosqlite.IntegrityError:
        raise BadRequestException("分类名称已存在")
    return CategoryOut(id=cursor.lastrowid, name=data.name, sort_order=data.sort_order)


async def update_category(cat_id: int, data: CategoryUpdate) -> CategoryOut:
    db = await get_db()
    cursor = await db.execute("SELECT id, name, sort_order FROM categories WHERE id = ?", (cat_id,))
    row = await cursor.fetchone()
    if not row:
        raise NotFoundException("分类不存在")
    name = data.name if data.name is not None else row["name"]
    sort_order = data.sort_order if data.sort_order is not None else row["sort_order"]
    try:
        await db.execute(
            "UPDATE categories SET name = ?, sort_order = ? WHERE id = ?",
            (name, sort_order, cat_id),
        )
        await db.commit()
    except aiosqlite.IntegrityError:
        raise BadRequestException("分类名称已存在")
    return CategoryOut(id=cat_id, name=name, sort_order=sort_order)


async def delete_category(cat_id: int) -> None:
    db = await get_db()
    cursor = await db.execute("SELECT id FROM categories WHERE id = ?", (cat_id,))
    if not await cursor.fetchone():
        raise NotFoundException("分类不存在")
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM resources WHERE category_id = ?", (cat_id,))
    row = await cursor.fetchone()
    if row["cnt"] > 0:
        raise BadRequestException("该分类下有资源，无法删除")
    await db.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
    await db.commit()
