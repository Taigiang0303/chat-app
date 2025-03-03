from typing import List, Optional
from pydantic import BaseSettings, validator, AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "Auth Service"
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    
    @property
    def DATABASE_URI(self) -> str:
        """Alias for DATABASE_URL for backward compatibility"""
        return self.DATABASE_URL
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    JWT_SECRET: str = "dev_secret_key_for_testing_only"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Security
    PASSWORD_HASH_ROUNDS: int = 12
    
    # Supabase
    SUPABASE_URL: str = "https://mock.supabase.co"
    SUPABASE_SERVICE_ROLE_KEY: str = "mock_key"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings() 