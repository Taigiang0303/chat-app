from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID, uuid4


class UserBase(BaseModel):
    """Base user model with common fields"""
    email: EmailStr
    display_name: str = Field(..., min_length=2, max_length=50)
    is_active: bool = True


class UserCreate(UserBase):
    """Model for user creation with password"""
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v


class UserUpdate(BaseModel):
    """Model for user updates"""
    email: Optional[EmailStr] = None
    display_name: Optional[str] = Field(None, min_length=2, max_length=50)
    profile_image_url: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """Model for user in database"""
    id: UUID = Field(default_factory=uuid4)
    hashed_password: str
    profile_image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    supabase_uid: Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    """Public user model without sensitive information"""
    id: UUID
    profile_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserWithToken(User):
    """User model with authentication token"""
    access_token: str
    token_type: str = "bearer" 