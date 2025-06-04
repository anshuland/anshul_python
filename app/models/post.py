from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from app.models.user import User

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    author_id: int = Field(foreign_key="user.id")
    author: Optional["User"] = Relationship(back_populates="posts")

    comments: List["Comment"] = Relationship(back_populates="post")
    likes: List["Like"] = Relationship(back_populates="post")

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    post_id: int = Field(foreign_key="post.id")
    user_id: int = Field(foreign_key="user.id")

    post: Optional["Post"] = Relationship(back_populates="comments")
    user: Optional["User"] = Relationship(back_populates="comments")

class Like(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    user_id: int = Field(foreign_key="user.id")

    post: Optional["Post"] = Relationship(back_populates="likes")
    user: Optional["User"] = Relationship(back_populates="likes")