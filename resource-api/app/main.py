from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from app.database import init_db, close_db
from app.middleware.error_handler import AppException
from app.config import UPLOAD_DIR
from app.routers import auth, categories, resources, upload, favorites, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(title="资源分享站 API", version="1.0.0", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploads
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Exception handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.code, content={"code": exc.code, "message": exc.message, "data": None})

# Routers
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(resources.router)
app.include_router(upload.router)
app.include_router(favorites.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {"code": 0, "message": "资源分享站 API 运行中", "data": None}
