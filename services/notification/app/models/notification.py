from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import JSON


class NotificationType(str, Enum):
    """Enum for notification types"""
    SYSTEM = "system"
    CHAT = "chat"
    FRIEND_REQUEST = "friend_request"
    MENTION = "mention"
    ALERT = "alert"


class NotificationStatus(str, Enum):
    """Enum for notification status"""
    PENDING = "pending"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class NotificationBase(SQLModel):
    """Base model for notification"""
    type: NotificationType = Field(default=NotificationType.SYSTEM)
    title: str = Field(max_length=255)
    content: str
    recipient_id: str = Field(index=True)
    sender_id: Optional[str] = Field(default=None, index=True)
    reference_id: Optional[str] = Field(default=None, description="ID of the related entity (chat, friend request, etc.)")
    reference_type: Optional[str] = Field(default=None, description="Type of the related entity")
    status: NotificationStatus = Field(default=NotificationStatus.PENDING)
    is_read: bool = Field(default=False)
    metadata: Optional[dict] = Field(default=None, sa_column=Field(JSON))


class Notification(NotificationBase, table=True):
    """Notification model for database"""
    __tablename__ = "notifications"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    delivered_at: Optional[datetime] = Field(default=None)
    read_at: Optional[datetime] = Field(default=None)


class NotificationCreate(NotificationBase):
    """Schema for creating a notification"""
    pass


class NotificationRead(NotificationBase):
    """Schema for reading a notification"""
    id: int
    created_at: datetime
    updated_at: datetime
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None


class NotificationUpdate(SQLModel):
    """Schema for updating a notification"""
    status: Optional[NotificationStatus] = None
    is_read: Optional[bool] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None 