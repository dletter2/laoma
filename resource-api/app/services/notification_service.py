import httpx
import json
from app.database import get_db


async def get_setting(key: str) -> str | None:
    db = await get_db()
    cursor = await db.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = await cursor.fetchone()
    return row["value"] if row else None


async def set_setting(key: str, value: str) -> None:
    db = await get_db()
    await db.execute(
        "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?",
        (key, value, value),
    )
    await db.commit()


async def notify_new_resource(title: str, summary: str, uploader_name: str) -> None:
    webhook_url = await get_setting("dingtalk_webhook")
    if not webhook_url:
        return
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(webhook_url, json={
                "msgtype": "markdown",
                "markdown": {
                    "title": "新资源提交通知",
                    "text": (
                        f"### 新资源提交通知\n\n"
                        f"- **标题**: {title}\n"
                        f"- **描述**: {summary or '无'}\n"
                        f"- **上传人**: {uploader_name}\n\n"
                        f"请登录后台审核"
                    ),
                },
            })
    except Exception:
        pass
