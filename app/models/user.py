from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
#from app.models import User, Post, Comment, Like


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password: str
    full_name: Optional[str] = None
    profile_picture: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    posts: List["Post"] = Relationship(back_populates="author", sa_relationship_kwargs={"cascade": "all, delete"})
    comments: List["Comment"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})
    likes: List["Like"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})
