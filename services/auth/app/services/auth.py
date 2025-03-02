from datetime import datetime, timedelta
from typing import Optional, Union
from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db import get_session
from app.db.repositories import UserRepository, RefreshTokenRepository
from app.models.token import TokenPayload
from app.models.user import User, UserCreate, UserInDB

# Password hashing context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# Repositories
user_repository = UserRepository()
refresh_token_repository = RefreshTokenRepository()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> Optional[User]:
    """Authenticate a user by email and password"""
    user = await user_repository.get_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(
    subject: Union[str, UUID], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def create_refresh_token(
    subject: Union[str, UUID], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT refresh token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh",
        "jti": str(uuid4()),  # Unique token ID
    }
    
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


async def get_current_user(
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> User:
    """Get the current authenticated user from a JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        # Check token type
        if token_data.type != "access":
            raise credentials_exception
        
        # Check token expiration
        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise credentials_exception
            
        user_id = token_data.sub
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_repository.get(db, UUID(user_id))
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user


async def register_new_user(
    db: AsyncSession, user_in: UserCreate
) -> User:
    """Register a new user"""
    # Check if user with this email already exists
    existing_user = await user_repository.get_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create new user
    hashed_password = get_password_hash(user_in.password)
    user_data = user_in.dict()
    user_data.pop("password")
    user_data["hashed_password"] = hashed_password
    
    user = await user_repository.create(db, obj_in=UserInDB(**user_data))
    return user


async def create_user_refresh_token(
    db: AsyncSession, user_id: UUID
) -> str:
    """Create a refresh token for a user"""
    # Generate refresh token
    refresh_token = create_refresh_token(user_id)
    
    # Parse token to get expiration
    payload = jwt.decode(
        refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    expires_at = datetime.fromtimestamp(payload["exp"])
    
    # Store in database
    await refresh_token_repository.create(
        db, user_id=user_id, token=refresh_token, expires_at=expires_at
    )
    
    return refresh_token


async def refresh_access_token(
    db: AsyncSession, refresh_token: str
) -> dict:
    """Refresh an access token using a refresh token"""
    try:
        # Decode token
        payload = jwt.decode(
            refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Validate token type
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        
        # Get token from database
        token_in_db = await refresh_token_repository.get_by_token(db, refresh_token)
        if not token_in_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        
        # Check if token is revoked
        if token_in_db.revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked",
            )
        
        # Check if token is expired
        if token_in_db.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired",
            )
        
        # Get user
        user_id = UUID(payload.get("sub"))
        user = await user_repository.get(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        # Create new access token
        access_token = create_access_token(user.id)
        
        # Create new refresh token (token rotation)
        new_refresh_token = await create_user_refresh_token(db, user.id)
        
        # Revoke old refresh token
        await refresh_token_repository.revoke(db, token_in_db.id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "refresh_token": new_refresh_token,
        }
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) 