from typing import List, Optional
from pydantic import BaseSettings, validator, AnyHttpUrl, EmailStr


class Settings(BaseSettings):
    PROJECT_NAME: str = "Notification Service"
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/2"
    
    # NATS
    NATS_URL: str = "nats://localhost:4222"
    
    # JWT
    JWT_SECRET: str = "dev_secret_key_for_testing_only"
    JWT_ALGORITHM: str = "HS256"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Email
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = False
    SMTP_SSL: bool = False
    EMAIL_FROM: str = "noreply@example.com"
    EMAIL_FROM_NAME: str = "Advanced Chat"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings() 