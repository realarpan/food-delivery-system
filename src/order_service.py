from datetime import datetime
from typing import List, Dict, Optional

class OrderService:
    """Service for managing food delivery orders."""
    
    def __init__(self):
        self.orders = {}
        self.order_counter = 0
    
    def create_order(self, user_id: int, items: List[Dict], address: str) -> Dict:
        """Create new order."""
        self.order_counter += 1
        order = {
            "id": self.order_counter,
            "user_id": user_id,
            "items": items,
            "address": address,
            "status": "PENDING",
            "created_at": datetime.now().isoformat(),
            "total": sum(item["price"] * item["qty"] for item in items)
        }
        self.orders[self.order_counter] = order
        return order
    
    def get_order(self, order_id: int) -> Optional[Dict]:
        """Get order by ID."""
        return self.orders.get(order_id)
    
    def update_status(self, order_id: int, status: str) -> bool:
        """Update order status."""
        if order_id in self.orders:
            self.orders[order_id]["status"] = status
            return True
        return False
    
    def get_user_orders(self, user_id: int) -> List[Dict]:
        """Get all orders for user."""
        return [o for o in self.orders.values() if o["user_id"] == user_id]
