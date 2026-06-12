import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db, get_db, close_db
from app.services.auth_service import hash_password


async def seed():
    await init_db()
    db = await get_db()
    # seed admin
    cursor = await db.execute("SELECT id FROM users WHERE username = 'admin'")
    if not await cursor.fetchone():
        await db.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("admin", hash_password("admin123"), "admin"),
        )
        print("Created admin user: admin / admin123")
    else:
        print("Admin user already exists")
    # seed categories
    categories = [
        ("教程资料", 1),
        ("软件工具", 2),
        ("模板素材", 3),
        ("文档报告", 4),
        ("设计资源", 5),
        ("其他", 6),
    ]
    for name, sort_order in categories:
        cursor = await db.execute("SELECT id FROM categories WHERE name = ?", (name,))
        if not await cursor.fetchone():
            await db.execute("INSERT INTO categories (name, sort_order) VALUES (?, ?)", (name, sort_order))
            print(f"Created category: {name}")
    await db.commit()
    await close_db()
    print("Seed data complete!")


if __name__ == "__main__":
    asyncio.run(seed())
