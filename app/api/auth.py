from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user import UserCreate, UserRead, Token, TokenRefreshRequest
from app.crud import user as user_crud
from app.core.database import async_session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token

router = APIRouter(prefix="/auth", tags=["auth"])

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await user_crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    existing = await user_crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = await user_crud.create_user(db, user)
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh_token(payload: TokenRefreshRequest):
    decoded = decode_token(payload.refresh_token)
    if not decoded or decoded.get("token_type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    username = decoded.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token payload")

    new_access_token = create_access_token(data={"sub": username})
    new_refresh_token = create_refresh_token(data={"sub": username})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
