"""
Mock Supabase adapter for authentication service.
This adapter provides mock methods to simulate Supabase for user management and authentication.
"""

import os
from typing import Optional, Dict, Any
# Removed supabase import

from app.core.config import settings
from app.models.user import UserCreate, User

class MockSupabaseAdapter:
    """Mock adapter for Supabase authentication and database operations"""
    
    def __init__(self):
        self.supabase_url = "https://mock.supabase.co"
        self.supabase_key = "mock_key"
        # Mock in-memory storage
        self.users = {}
    
    async def sign_up(self, email: str, password: str, user_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock register a new user
        
        Args:
            email: User's email
            password: User's password
            user_metadata: Additional user metadata
            
        Returns:
            Dict containing user data and session
        """
        user_id = str(len(self.users) + 1)
        user = {
            "id": user_id,
            "email": email,
            "user_metadata": user_metadata
        }
        self.users[user_id] = user
        return {
            "user": user,
            "session": {
                "access_token": f"mock_token_{user_id}",
                "refresh_token": f"mock_refresh_{user_id}"
            }
        }
    
    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """
        Mock sign in a user
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            Dict containing user data and session
        """
        # Find user by email
        user = next((u for u in self.users.values() if u["email"] == email), None)
        if not user:
            # For testing, create a mock user if not found
            user_id = str(len(self.users) + 1)
            user = {
                "id": user_id,
                "email": email,
                "user_metadata": {}
            }
            self.users[user_id] = user
            
        return {
            "user": user,
            "session": {
                "access_token": f"mock_token_{user['id']}",
                "refresh_token": f"mock_refresh_{user['id']}"
            }
        }
    
    async def sign_out(self, access_token: str) -> None:
        """
        Mock sign out a user
        
        Args:
            access_token: User's access token
        """
        # No-op in mock implementation
        pass
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Mock get user data
        
        Args:
            user_id: User's ID
            
        Returns:
            User data or None if not found
        """
        return self.users.get(user_id)
    
    async def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock update user data
        
        Args:
            user_id: User's ID
            user_data: Updated user data
            
        Returns:
            Updated user data
        """
        if user_id in self.users:
            self.users[user_id].update(user_data)
            return self.users[user_id]
        return {}

# Create a singleton instance
supabase_adapter = MockSupabaseAdapter() 