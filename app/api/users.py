from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user, get_password_hash
from app.schemas.user import UserRead, UserUpdate
from app.models.user import User
import shutil, os
from uuid import uuid4

router = APIRouter(prefix="/users", tags=["users"])

'''async def get_db():
    async with async_session() as session:
        yield session'''

# View own profile
@router.get("/me", response_model=UserRead)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Update profile (name/password)
@router.put("/me", response_model=UserRead)
async def update_profile(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    if user_update.password:
        current_user.password = get_password_hash(user_update.password)

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

# Upload profile picture
@router.post("/me/upload", response_model=UserRead)
async def upload_profile_picture(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Save image with random filename
    extension = file.filename.split(".")[-1]
    filename = f"{uuid4().hex}.{extension}"
    filepath = f"app/static/profile_pics/{filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    current_user.profile_picture = f"/static/profile_pics/{filename}"
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

# Delete account
@router.delete("/me", status_code=204)
async def delete_account(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await db.delete(current_user)
    await db.commit()
    return
