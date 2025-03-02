from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.exceptions import AuthenticationError

# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a password hash"""
    return pwd_context.hash(password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT refresh token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """Decode a JWT token"""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.JWTError:
        raise AuthenticationError("Invalid token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current user from the token"""
    try:
        payload = decode_token(token)
        token_type = payload.get("type")
        if token_type != "access":
            raise AuthenticationError("Invalid token type")
        
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthenticationError("Invalid token")
        
        # Here you would typically fetch the user from the database
        # For now, we'll just return the user_id
        return user_id
    except AuthenticationError as e:
        raise e
    except Exception:
        raise AuthenticationError("Could not validate credentials") 