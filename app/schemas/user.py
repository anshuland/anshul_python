from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    profile_picture: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TokenRefreshRequest(BaseModel):
    refresh_token: str
