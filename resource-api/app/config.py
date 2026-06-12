import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.getenv("DB_PATH", "/data/laoma/db/app.db")
DATA_DIR = os.path.dirname(DB_PATH)

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "resource-share-site-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # 2 hours
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Pagination
DEFAULT_PAGE_SIZE = 12

# ensure directories
os.makedirs(DATA_DIR, exist_ok=True)
