import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.response import BaseResponse
from app.config import UPLOAD_DIR, MAX_UPLOAD_SIZE

router = APIRouter(prefix="/api/v1/upload", tags=["upload"])


@router.post("")
async def upload_file(file: UploadFile = File(...)):
    if file.size and file.size > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="文件大小不能超过200MB")
    ext = os.path.splitext(file.filename or "")[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="文件大小不能超过200MB")
    with open(filepath, "wb") as f:
        f.write(content)
    file_url = f"/uploads/{filename}"
    return BaseResponse(data={"url": file_url, "size": len(content), "filename": file.filename})
