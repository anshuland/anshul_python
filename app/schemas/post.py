from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    #title: Optional[str]
    title: str
    content: Optional[str]

class CommentCreate(BaseModel):
    text: str

class CommentRead(BaseModel):
    id: int
    text: str
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
