from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db import get_session
from app.db.repositories import refresh_token_repository
from app.models.token import TokenResponse
from app.models.user import User, UserCreate, UserWithToken
from app.services.auth import (
    authenticate_user,
    create_access_token,
    create_user_refresh_token,
    get_current_user,
    refresh_access_token,
    register_new_user,
)

router = APIRouter()


@router.post("/register", response_model=UserWithToken, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_session),
):
    """
    Register a new user
    """
    user = await register_new_user(db, user_in)
    
    # Create access token
    access_token = create_access_token(user.id)
    
    # Create refresh token
    refresh_token = await create_user_refresh_token(db, user.id)
    
    return {
        **user.dict(),
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(user.id)
    
    # Create refresh token
    refresh_token = await create_user_refresh_token(db, user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_token": refresh_token,
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_session),
):
    """
    Refresh access token
    """
    return await refresh_access_token(db, refresh_token)


@router.post("/logout")
async def logout(
    refresh_token: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Logout user by revoking refresh token
    """
    token = await refresh_token_repository.get_by_token(db, refresh_token)
    if token and token.user_id == current_user.id:
        await refresh_token_repository.revoke(db, token.id)
    
    return {"detail": "Successfully logged out"}


@router.post("/logout-all")
async def logout_all(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Logout user from all devices by revoking all refresh tokens
    """
    await refresh_token_repository.revoke_all_for_user(db, current_user.id)
    
    return {"detail": "Successfully logged out from all devices"}