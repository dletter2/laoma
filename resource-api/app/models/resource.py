from pydantic import BaseModel


class ResourceCreate(BaseModel):
    title: str
    summary: str = ""
    category_id: int
    tags: str = ""
    link: str = ""
    link_password: str = ""
    file_size: float = 0


class ResourceUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    category_id: int | None = None
    tags: str | None = None
    link: str | None = None
    link_password: str | None = None
    file_size: float | None = None
    is_hot: int | None = None
    status: str | None = None


class ResourceOut(BaseModel):
    id: int
    title: str
    summary: str
    category_id: int
    category_name: str = ""
    tags: str
    link: str
    link_password: str
    file_size: int
    upload_time: str | None = None
    is_hot: int
    view_count: int
    favorite_count: int
    uploader_id: int
    uploader_nickname: str = ""
    status: str


class ResourceStatusUpdate(BaseModel):
    status: str  # approved, rejected, published, unpublished


class BatchStatusUpdate(BaseModel):
    ids: list[int]
    status: str


class BatchDelete(BaseModel):
    ids: list[int]


class UserStatusUpdate(BaseModel):
    status: str  # active, disabled
