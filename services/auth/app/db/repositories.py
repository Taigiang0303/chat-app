from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.base import BaseRepository
from app.db.models import User, RefreshToken
from app.models.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """User repository for database operations"""

    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get a user by email"""
        statement = select(User).where(User.email == email)
        results = await db.execute(statement)
        return results.scalar_one_or_none()


class RefreshTokenRepository:
    """Refresh token repository for database operations"""

    async def create(
        self, db: AsyncSession, *, user_id: UUID, token: str, expires_at: str
    ) -> RefreshToken:
        """Create a new refresh token"""
        db_obj = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_token(self, db: AsyncSession, token: str) -> Optional[RefreshToken]:
        """Get a refresh token by token value"""
        statement = select(RefreshToken).where(RefreshToken.token == token)
        results = await db.execute(statement)
        return results.scalar_one_or_none()

    async def revoke(self, db: AsyncSession, token_id: UUID) -> Optional[RefreshToken]:
        """Revoke a refresh token"""
        statement = select(RefreshToken).where(RefreshToken.id == token_id)
        results = await db.execute(statement)
        token = results.scalar_one_or_none()
        if token:
            token.is_revoked = True
            db.add(token)
            await db.commit()
            await db.refresh(token)
        return token

    async def revoke_all_for_user(self, db: AsyncSession, user_id: UUID) -> None:
        """Revoke all refresh tokens for a user"""
        statement = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False,
        )
        results = await db.execute(statement)
        tokens = results.scalars().all()
        for token in tokens:
            token.is_revoked = True
            db.add(token)
        await db.commit() 