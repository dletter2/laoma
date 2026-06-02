from pydantic import BaseModel


class ResourceCreate(BaseModel):
    title: str
    summary: str = ""
    category_id: int
    cover_url: str = ""
    tags: str = ""
    file_size: int = 0
    file_path: str = ""


class ResourceUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    category_id: int | None = None
    cover_url: str | None = None
    tags: str | None = None
    is_hot: int | None = None
    status: str | None = None


class ResourceOut(BaseModel):
    id: int
    title: str
    summary: str
    category_id: int
    category_name: str = ""
    cover_url: str
    tags: str
    file_size: int
    upload_time: str | None = None
    is_hot: int
    view_count: int
    favorite_count: int
    uploader_id: int
    status: str


class ResourceStatusUpdate(BaseModel):
    status: str  # approved, rejected, published, unpublished


class UserStatusUpdate(BaseModel):
    status: str  # active, disabled
