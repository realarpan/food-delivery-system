"""
Custom exception classes for the food delivery system.
Provides domain-specific exceptions for error handling.
"""

class FoodDeliveryException(Exception):
    """Base exception for all food delivery system errors."""
    def __init__(self, message: str, code: str = "ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class AuthenticationError(FoodDeliveryException):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTH_ERROR")

class AuthorizationError(FoodDeliveryException):
    """Raised when user lacks required permissions."""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, "AUTH_DENIED")

class ValidationError(FoodDeliveryException):
    """Raised when input validation fails."""
    def __init__(self, message: str = "Validation failed", field: str = None):
        self.field = field
        super().__init__(message, "VALIDATION_ERROR")

class ResourceNotFoundError(FoodDeliveryException):
    """Raised when a resource is not found."""
    def __init__(self, resource: str = "Resource", resource_id: str = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" (ID: {resource_id})"
        super().__init__(message, "NOT_FOUND")

class DuplicateResourceError(FoodDeliveryException):
    """Raised when trying to create duplicate resource."""
    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} already exists", "DUPLICATE")

class OrderError(FoodDeliveryException):
    """Raised for order-related errors."""
    def __init__(self, message: str = "Order error"):
        super().__init__(message, "ORDER_ERROR")

class InsufficientInventoryError(FoodDeliveryException):
    """Raised when item is out of stock."""
    def __init__(self, item: str = "Item"):
        super().__init__(f"{item} is out of stock", "OUT_OF_STOCK")

class DatabaseError(FoodDeliveryException):
    """Raised for database operation failures."""
    def __init__(self, message: str = "Database error"):
        super().__init__(message, "DB_ERROR")

class DeliveryError(FoodDeliveryException):
    """Raised for delivery-related errors."""
    def __init__(self, message: str = "Delivery error"):
        super().__init__(message, "DELIVERY_ERROR")

class PaymentError(FoodDeliveryException):
    """Raised for payment processing errors."""
    def __init__(self, message: str = "Payment failed"):
        super().__init__(message, "PAYMENT_ERROR")

class ConfigurationError(FoodDeliveryException):
    """Raised for missing or invalid configuration."""
    def __init__(self, config_key: str = None):
        message = "Configuration error"
        if config_key:
            message += f": {config_key}"
        super().__init__(message, "CONFIG_ERROR")
