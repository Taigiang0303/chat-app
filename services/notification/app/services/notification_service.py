import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundError, NotificationDeliveryError
from app.models.notification import Notification, NotificationStatus, NotificationType
from app.repositories.notification_repository import NotificationRepository


logger = logging.getLogger(__name__)


class NotificationService:
    """Service for handling notification business logic"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = NotificationRepository(session)
    
    async def create_notification(self, notification_data: Dict[str, Any]) -> Notification:
        """Create a new notification"""
        return await self.repository.create(notification_data)
    
    async def get_notification(self, notification_id: int) -> Notification:
        """Get a notification by ID"""
        notification = await self.repository.get_by_id(notification_id)
        if not notification:
            raise ResourceNotFoundError(f"Notification with ID {notification_id} not found")
        return notification
    
    async def get_notifications_for_recipient(
        self, 
        recipient_id: str, 
        skip: int = 0, 
        limit: int = 100,
        include_read: bool = False
    ) -> List[Notification]:
        """Get notifications for a recipient"""
        return await self.repository.get_by_recipient(
            recipient_id=recipient_id,
            skip=skip,
            limit=limit,
            include_read=include_read
        )
    
    async def mark_as_read(self, notification_id: int) -> Notification:
        """Mark a notification as read"""
        notification = await self.repository.mark_as_read(notification_id)
        if not notification:
            raise ResourceNotFoundError(f"Notification with ID {notification_id} not found")
        return notification
    
    async def mark_all_as_read(self, recipient_id: str) -> int:
        """Mark all notifications for a recipient as read"""
        return await self.repository.mark_all_as_read(recipient_id)
    
    async def delete_notification(self, notification_id: int) -> bool:
        """Delete a notification"""
        result = await self.repository.delete(notification_id)
        if not result:
            raise ResourceNotFoundError(f"Notification with ID {notification_id} not found")
        return result
    
    async def count_unread_notifications(self, recipient_id: str) -> int:
        """Count unread notifications for a recipient"""
        return await self.repository.count_unread(recipient_id)
    
    async def create_system_notification(
        self,
        recipient_id: str,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """Create a system notification"""
        notification_data = {
            "type": NotificationType.SYSTEM,
            "title": title,
            "content": content,
            "recipient_id": recipient_id,
            "metadata": metadata or {}
        }
        return await self.create_notification(notification_data)
    
    async def create_chat_notification(
        self,
        recipient_id: str,
        sender_id: str,
        chat_id: str,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """Create a chat notification"""
        notification_data = {
            "type": NotificationType.CHAT,
            "title": title,
            "content": content,
            "recipient_id": recipient_id,
            "sender_id": sender_id,
            "reference_id": chat_id,
            "reference_type": "chat",
            "metadata": metadata or {}
        }
        return await self.create_notification(notification_data)
    
    async def create_friend_request_notification(
        self,
        recipient_id: str,
        sender_id: str,
        request_id: str,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """Create a friend request notification"""
        notification_data = {
            "type": NotificationType.FRIEND_REQUEST,
            "title": title,
            "content": content,
            "recipient_id": recipient_id,
            "sender_id": sender_id,
            "reference_id": request_id,
            "reference_type": "friend_request",
            "metadata": metadata or {}
        }
        return await self.create_notification(notification_data)
    
    async def process_pending_notifications(self, limit: int = 100) -> List[Notification]:
        """Process pending notifications"""
        pending_notifications = await self.repository.get_pending_notifications(limit)
        processed_notifications = []
        
        for notification in pending_notifications:
            try:
                # Here you would implement the actual delivery logic
                # For example, sending an email, push notification, etc.
                logger.info(f"Processing notification {notification.id} for recipient {notification.recipient_id}")
                
                # Mark as delivered
                processed_notification = await self.repository.mark_as_delivered(notification.id)
                if processed_notification:
                    processed_notifications.append(processed_notification)
                
            except Exception as e:
                logger.error(f"Failed to process notification {notification.id}: {str(e)}")
                await self.repository.mark_as_failed(notification.id, str(e))
        
        return processed_notifications 