from pydantic import BaseModel


class ShareCreate(BaseModel):
    name: str
    url: str
    avatar_url: str = ""
    description: str = ""
    sort_order: int = 0


class ShareUpdate(BaseModel):
    name: str | None = None
    url: str | None = None
    avatar_url: str | None = None
    description: str | None = None
    sort_order: int | None = None


class ShareOut(BaseModel):
    id: int
    name: str
    url: str
    avatar_url: str
    description: str
    sort_order: int
    created_at: str | None = None
    updated_at: str | None = None
