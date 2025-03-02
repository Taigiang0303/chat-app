from datetime import datetime
from typing import List, Optional, Dict, Any

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from app.models.notification import Notification, NotificationStatus, NotificationType


class NotificationRepository:
    """Repository for notification data operations"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, notification_data: Dict[str, Any]) -> Notification:
        """Create a new notification"""
        notification = Notification(**notification_data)
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification
    
    async def get_by_id(self, notification_id: int) -> Optional[Notification]:
        """Get a notification by ID"""
        result = await self.session.execute(
            select(Notification).where(Notification.id == notification_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_recipient(
        self, 
        recipient_id: str, 
        skip: int = 0, 
        limit: int = 100,
        include_read: bool = False
    ) -> List[Notification]:
        """Get notifications for a recipient"""
        query = select(Notification).where(Notification.recipient_id == recipient_id)
        
        if not include_read:
            query = query.where(Notification.is_read == False)
            
        query = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def mark_as_read(self, notification_id: int) -> Optional[Notification]:
        """Mark a notification as read"""
        notification = await self.get_by_id(notification_id)
        if not notification:
            return None
            
        notification.is_read = True
        notification.status = NotificationStatus.READ
        notification.read_at = datetime.utcnow()
        notification.updated_at = datetime.utcnow()
        
        await self.session.commit()
        await self.session.refresh(notification)
        return notification
    
    async def mark_as_delivered(self, notification_id: int) -> Optional[Notification]:
        """Mark a notification as delivered"""
        notification = await self.get_by_id(notification_id)
        if not notification:
            return None
            
        notification.status = NotificationStatus.DELIVERED
        notification.delivered_at = datetime.utcnow()
        notification.updated_at = datetime.utcnow()
        
        await self.session.commit()
        await self.session.refresh(notification)
        return notification
    
    async def mark_as_failed(self, notification_id: int, error_message: str = None) -> Optional[Notification]:
        """Mark a notification as failed"""
        notification = await self.get_by_id(notification_id)
        if not notification:
            return None
            
        notification.status = NotificationStatus.FAILED
        notification.updated_at = datetime.utcnow()
        
        if error_message and notification.metadata is None:
            notification.metadata = {}
            
        if error_message and notification.metadata is not None:
            notification.metadata["error"] = error_message
        
        await self.session.commit()
        await self.session.refresh(notification)
        return notification
    
    async def mark_all_as_read(self, recipient_id: str) -> int:
        """Mark all notifications for a recipient as read"""
        now = datetime.utcnow()
        result = await self.session.execute(
            update(Notification)
            .where(
                (Notification.recipient_id == recipient_id) & 
                (Notification.is_read == False)
            )
            .values(
                is_read=True, 
                status=NotificationStatus.READ,
                read_at=now,
                updated_at=now
            )
            .execution_options(synchronize_session=False)
        )
        await self.session.commit()
        return result.rowcount
    
    async def delete(self, notification_id: int) -> bool:
        """Delete a notification"""
        notification = await self.get_by_id(notification_id)
        if not notification:
            return False
            
        await self.session.delete(notification)
        await self.session.commit()
        return True
    
    async def count_unread(self, recipient_id: str) -> int:
        """Count unread notifications for a recipient"""
        result = await self.session.execute(
            select(func.count())
            .where(
                (Notification.recipient_id == recipient_id) & 
                (Notification.is_read == False)
            )
        )
        return result.scalar_one()
    
    async def get_pending_notifications(self, limit: int = 100) -> List[Notification]:
        """Get pending notifications for processing"""
        query = (
            select(Notification)
            .where(Notification.status == NotificationStatus.PENDING)
            .order_by(Notification.created_at)
            .limit(limit)
        )
        
        result = await self.session.execute(query)
        return result.scalars().all() 