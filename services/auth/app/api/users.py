from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.db.repositories import UserRepository
from app.models.user import User, UserUpdate
from app.services.auth import get_current_user

router = APIRouter()
user_repository = UserRepository()


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_user),
):
    """
    Get current user
    """
    return current_user


@router.put("/me", response_model=User)
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Update current user
    """
    user = await user_repository.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=User)
async def read_user_by_id(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Get a specific user by id
    """
    user = await user_repository.get(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/", response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Retrieve users
    """
    users = await user_repository.get_multi(db, skip=skip, limit=limit)
    return users 