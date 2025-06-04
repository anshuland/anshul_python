from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.core.database import async_session
from app.core.security import get_current_user
from app.models.post import Post, Comment, Like
from app.schemas.post import PostCreate, PostRead, PostUpdate, CommentCreate, CommentRead
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["posts"])

async def get_db():
    async with async_session() as session:
        yield session

# Create post
@router.post("/", response_model=PostRead)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    new_post = Post(title=post.title, content=post.content, author_id=user.id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

# Get all posts
@router.get("/", response_model=list[PostRead])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.exec(select(Post))
    return result.all()

# Update post
@router.put("/{post_id}", response_model=PostRead)
async def update_post(post_id: int, update: PostUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    post = await db.get(Post, post_id)
    print("UPDATE OBJECT:", update)

    if not post or post.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    if update.title:
        post.title = update.title
    if update.content:
        post.content = update.content
    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post

# Delete post
@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    post = await db.get(Post, post_id)
    if not post or post.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await db.delete(post)
    await db.commit()
    return

# Comment on post
@router.post("/{post_id}/comment", response_model=CommentRead)
async def add_comment(post_id: int, comment: CommentCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    new_comment = Comment(text=comment.text, post_id=post_id, user_id=user.id)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment

# Like post
@router.post("/{post_id}/like")
async def like_post(post_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    existing_like = await db.exec(select(Like).where(Like.post_id == post_id, Like.user_id == user.id))
    if existing_like.first():
        raise HTTPException(status_code=400, detail="Already liked")
    like = Like(post_id=post_id, user_id=user.id)
    db.add(like)
    await db.commit()
    return {"message": "Liked"}
