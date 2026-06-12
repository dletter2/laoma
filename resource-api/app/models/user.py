from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str
    nickname: str | None = None
    captcha_key: str = ""
    captcha_code: str = ""


class UserLogin(BaseModel):
    username: str
    password: str
    captcha_key: str = ""
    captcha_code: str = ""


class UserOut(BaseModel):
    id: int
    username: str
    nickname: str = ""
    role: str
    created_at: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class RefreshRequest(BaseModel):
    refresh_token: str
