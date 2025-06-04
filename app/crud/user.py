from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def get_user_by_username(session: AsyncSession, username: str):
    statement = select(User).where(User.username == username)
    result = await session.execute(statement)
    return result.scalars().first()

async def get_user_by_email(session: AsyncSession, email: str):
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalars().first()

async def create_user(session: AsyncSession, user_create: UserCreate):
    hashed_pw = get_password_hash(user_create.password)
    user = User(
        username=user_create.username,
        email=user_create.email,
        full_name=user_create.full_name,
        password=hashed_pw,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def update_profile_picture(db: AsyncSession, user_id: int, path: str):
    statement = select(User).where(User.id == user_id)
    result = await db.exec(statement)
    user = result.one_or_none()
    if user:
        user.profile_picture = path
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user

