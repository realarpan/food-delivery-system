from typing import Dict, Optional
from datetime import datetime

class DeliveryTracker:
    """Track delivery status and location."""
    
    def __init__(self):
        self.deliveries = {}
    
    def start_delivery(self, order_id: int, driver_id: int, lat: float, lng: float) -> Dict:
        """Start tracking delivery."""
        delivery = {
            "order_id": order_id,
            "driver_id": driver_id,
            "status": "IN_TRANSIT",
            "started_at": datetime.now().isoformat(),
            "current_lat": lat,
            "current_lng": lng
        }
        self.deliveries[order_id] = delivery
        return delivery
    
    def update_location(self, order_id: int, lat: float, lng: float) -> bool:
        """Update delivery location."""
        if order_id in self.deliveries:
            self.deliveries[order_id]["current_lat"] = lat
            self.deliveries[order_id]["current_lng"] = lng
            self.deliveries[order_id]["updated_at"] = datetime.now().isoformat()
            return True
        return False
    
    def complete_delivery(self, order_id: int) -> bool:
        """Mark delivery as complete."""
        if order_id in self.deliveries:
            self.deliveries[order_id]["status"] = "DELIVERED"
            self.deliveries[order_id]["delivered_at"] = datetime.now().isoformat()
            return True
        return False
    
    def get_delivery(self, order_id: int) -> Optional[Dict]:
        """Get delivery details."""
        return self.deliveries.get(order_id)
