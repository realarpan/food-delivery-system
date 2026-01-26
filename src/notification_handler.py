from typing import List, Dict
from datetime import datetime
from enum import Enum

class NotificationType(Enum):
    ORDER_PLACED = "ORDER_PLACED"
    ORDER_CONFIRMED = "ORDER_CONFIRMED"
    PREPARING = "PREPARING"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class NotificationHandler:
    """Handle user notifications for order updates."""
    
    def __init__(self):
        self.notifications: Dict[int, List[Dict]] = {}
    
    def send_notification(self, user_id: int, order_id: int, 
                         notif_type: NotificationType, message: str) -> bool:
        """Send notification to user."""
        if user_id not in self.notifications:
            self.notifications[user_id] = []
        
        notification = {
            "order_id": order_id,
            "type": notif_type.value,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        self.notifications[user_id].append(notification)
        return True
    
    def get_notifications(self, user_id: int, unread_only: bool = False) -> List[Dict]:
        """Get user notifications."""
        if user_id not in self.notifications:
            return []
        
        if unread_only:
            return [n for n in self.notifications[user_id] if not n["read"]]
        return self.notifications[user_id]
    
    def mark_as_read(self, user_id: int, index: int) -> bool:
        """Mark notification as read."""
        if user_id in self.notifications and 0 <= index < len(self.notifications[user_id]):
            self.notifications[user_id][index]["read"] = True
            return True
        return False
