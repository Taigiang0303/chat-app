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
from app.services.supabase_adapter import supabase_adapter

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
    try:
        # First try to authenticate with Supabase
        supabase_response = await supabase_adapter.sign_in(email, password)
        
        if supabase_response and supabase_response.user:
            # Check if user exists in our database
            user = await user_repository.get_by_email(db, email)
            if not user:
                # Create user in our database if it doesn't exist
                user_data = UserCreate(
                    email=email,
                    display_name=supabase_response.user.user_metadata.get("display_name", email.split("@")[0]),
                    password=password  # This will be hashed in the repository
                )
                user = await register_new_user(db, user_data)
            return user
    except Exception as e:
        # If Supabase authentication fails, fall back to local authentication
        print(f"Supabase authentication error: {str(e)}")
        
    # Fall back to local authentication
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
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
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
        "type": "refresh"
    }
    
    return jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
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
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
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
    # Check if user already exists
    existing_user = await user_repository.get_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Try to register with Supabase first
    try:
        supabase_response = await supabase_adapter.sign_up(
            user_in.email, user_in.password, user_in.display_name
        )

        # Log the response for debugging
        print(f"Supabase registration response: {supabase_response}")

        if not supabase_response or not hasattr(supabase_response, 'user'):
            print(f"Supabase registration error: {supabase_response}")
            # Continue with local registration if Supabase fails
    except Exception as e:
        print(f"Supabase registration exception: {str(e)}")
        # Continue with local registration if Supabase fails

    # Create user in local database
    hashed_password = get_password_hash(user_in.password)

    # Create a new UserCreate model with the user data
    user_in_db = UserInDB(
        id=str(uuid4()),
        email=user_in.email,
        display_name=user_in.display_name,
        hashed_password=hashed_password,
        is_active=True
    )

    # Create user in database
    user = await user_repository.create(db, obj_in=user_in_db)
    
    return user


async def create_user_refresh_token(
    db: AsyncSession, user_id: UUID
) -> str:
    """Create a refresh token for a user"""
    # Generate refresh token
    refresh_token = create_refresh_token(user_id)
    
    # Parse token to get expiration
    payload = jwt.decode(
        refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
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
            refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
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
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if token is revoked
        if token_in_db.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
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