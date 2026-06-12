import sqlite3
import random
from datetime import datetime, timedelta
import os

DB_PATH = os.getenv("DB_PATH", "/data/laoma/db/app.db")

# 常见中文姓氏
SURNAMES = [
    "王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴",
    "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗",
    "梁", "宋", "郑", "谢", "韩", "唐", "冯", "于", "董", "萧",
    "程", "曹", "袁", "邓", "许", "傅", "沈", "曾", "彭", "吕",
    "苏", "卢", "蒋", "蔡", "贾", "丁", "魏", "薛", "叶", "阎",
]

# 名字用字
NAME_CHARS = [
    "伟", "强", "磊", "洋", "勇", "军", "杰", "涛", "明", "超",
    "华", "飞", "平", "刚", "文", "辉", "力", "斌", "波", "宇",
    "浩", "凯", "健", "俊", "峰", "志", "鹏", "建", "龙", "芳",
    "娜", "敏", "静", "丽", "艳", "娟", "秀", "婷", "雪", "月",
    "佳", "雅", "美", "欣", "萍", "红", "玲", "桂", "兰", "英",
]

# 英文用户名常用词
ENGLISH_WORDS = [
    "happy", "sunny", "lucky", "star", "moon", "sun", "sky", "cloud", "wind", "rain",
    "snow", "flower", "tree", "river", "mountain", "sea", "forest", "garden", "park",
    "cat", "dog", "bird", "fish", "rabbit", "tiger", "dragon", "phoenix", "lion", "bear",
    "code", "dev", "tech", "data", "web", "app", "game", "music", "art", "photo",
    "book", "read", "write", "learn", "study", "work", "play", "run", "walk", "fly",
    "cool", "nice", "good", "best", "top", "max", "super", "fast", "smart", "bright",
]

# 昵称修饰词
NICK_ADJ = [
    "快乐", "开心", "阳光", "可爱", "聪明", "帅气", "美丽", "温柔",
    "活泼", "文静", "开朗", "大方", "优雅", "自信", "坚强", "勇敢",
    "小", "大", "老", "阿",
]

# 昵称名词
NICK_NOUN = [
    "猫", "狗", "兔", "鸟", "鱼", "龙", "虎", "熊", "猴",
    "花", "草", "风", "云", "雨", "雪", "月", "星", "光",
    "书生", "达人", "高手", "老师", "同学", "朋友", "侠客", "行者",
]


def generate_users(count=200):
    users = []
    used_usernames = set()
    used_nicknames = set()

    for i in range(count):
        # 生成唯一用户名
        while True:
            fmt = random.randint(0, 4)
            if fmt == 0:
                username = f"{random.choice(SURNAMES)}{random.choice(ENGLISH_WORDS)}{random.randint(1, 99)}"
            elif fmt == 1:
                username = f"{random.choice(ENGLISH_WORDS)}_{random.choice(SURNAMES)}{random.randint(10, 99)}"
            elif fmt == 2:
                username = f"{random.choice(SURNAMES)}_{random.randint(1000, 9999)}"
            elif fmt == 3:
                username = f"user_{random.choice(SURNAMES)}{random.randint(100, 999)}"
            else:
                username = f"{random.choice(SURNAMES)}{chr(random.randint(97, 122))}{random.randint(10, 99)}"
            if username not in used_usernames:
                used_usernames.add(username)
                break

        # 生成唯昵称
        while True:
            fmt = random.randint(0, 3)
            surname = random.choice(SURNAMES)
            if fmt == 0:
                nickname = f"{surname}{random.choice(NAME_CHARS)}{random.choice(NAME_CHARS)}"
            elif fmt == 1:
                nickname = f"{random.choice(NICK_ADJ)}{surname}{random.choice(NICK_NOUN)}"
            elif fmt == 2:
                nickname = f"{surname}{random.choice(NICK_NOUN)}"
            else:
                nickname = f"{random.choice(NICK_ADJ)}{surname}"
            if nickname not in used_nicknames:
                used_nicknames.add(nickname)
                break

        # 随机注册时间
        start = datetime(2023, 1, 1)
        end = datetime(2025, 12, 31)
        delta = end - start
        random_date = start + timedelta(days=random.randint(0, delta.days))
        created_at = random_date.strftime("%Y-%m-%d %H:%M:%S")

        users.append((username, nickname, created_at))

    return users


def main():
    password_hash = "$2b$12$.uyxZQgo1baxm00bl5eFAO8jY5RgrsB/QlPT1yLzIMfF0m0vjm4cS"

    print("正在生成用户数据...")
    users = generate_users(200)

    print(f"正在写入数据库: {DB_PATH}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 确保表存在
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            nickname TEXT NOT NULL DEFAULT '',
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            status TEXT NOT NULL DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.executemany(
        "INSERT INTO users (username, nickname, password_hash, role, status, created_at) VALUES (?, ?, ?, 'user', 'active', ?)",
        [(u, n, password_hash, d) for u, n, d in users]
    )
    conn.commit()

    count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()

    print(f"\n成功导入 200 个用户，当前数据库共 {count} 个用户")
    print(f"密码统一为: Z15288472980q")
    print("\n前10个用户示例:")
    for i, (username, nickname, created_at) in enumerate(users[:10]):
        print(f"  {i+1}. 用户名: {username:<25} 昵称: {nickname:<10} 注册时间: {created_at}")


if __name__ == "__main__":
    main()
