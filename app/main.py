from fastapi.staticfiles import StaticFiles
from app.api import users, auth, posts
from fastapi import FastAPI
import app.models.init_models 
from sqlmodel import SQLModel
from app.core.database import engine

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
