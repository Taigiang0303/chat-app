from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Token(BaseModel):
    """Token model for authentication"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    """Token payload model"""
    sub: str  # User ID
    exp: datetime
    iat: Optional[datetime] = None
    jti: Optional[str] = None  # JWT ID for token identification
    type: str = "access"  # Token type: access or refresh


class RefreshToken(BaseModel):
    """Refresh token model"""
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_revoked: bool = False

    class Config:
        orm_mode = True


class TokenRequest(BaseModel):
    """Token request model"""
    grant_type: str
    username: Optional[str] = None
    password: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None 