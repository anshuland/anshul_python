from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_db():
    async with async_session() as session:
        yield session
