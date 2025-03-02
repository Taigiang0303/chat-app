from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel, select

from app.core.config import settings

# Create async engine for SQLModel
engine = create_async_engine(
    settings.DATABASE_URI,
    echo=settings.ENVIRONMENT == "development",
    future=True,
)

# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    """Get a new database session"""
    async with async_session() as session:
        yield session


# Define generic model type
ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository with CRUD operations
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize with SQLModel model class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: UUID) -> Optional[ModelType]:
        """
        Get a record by ID
        """
        statement = select(self.model).where(self.model.id == id)
        results = await db.execute(statement)
        return results.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination
        """
        statement = select(self.model).offset(skip).limit(limit)
        results = await db.execute(statement)
        return results.scalars().all()

    async def create(
        self, db: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        """
        Create a new record
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update a record
        """
        obj_data = db_obj.dict()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: UUID) -> ModelType:
        """
        Delete a record
        """
        statement = select(self.model).where(self.model.id == id)
        results = await db.execute(statement)
        obj = results.scalar_one_or_none()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj 