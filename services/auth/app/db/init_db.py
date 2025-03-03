import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    """Initialize the database with required tables"""
    logger.info("Creating database tables...")
    
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL)
    
    # Define SQL statements for creating tables
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        display_name VARCHAR(255) NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        profile_image_url VARCHAR(255),
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
    );
    """
    
    create_refresh_tokens_table = """
    CREATE TABLE IF NOT EXISTS refresh_tokens (
        id UUID PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        token VARCHAR(255) UNIQUE NOT NULL,
        expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
        is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """
    
    # Execute SQL statements
    async with engine.begin() as conn:
        logger.info("Creating users table...")
        await conn.execute(text(create_users_table))
        
        logger.info("Creating refresh_tokens table...")
        await conn.execute(text(create_refresh_tokens_table))
    
    logger.info("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db()) 