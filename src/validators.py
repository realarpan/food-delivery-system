"""
==================================================================================
VALIDATORS MODULE
==================================================================================
Comprehensive validation utilities for user input, order data, and food items.
Provides functions for validating email, phone, addresses, prices, and quantities.

Author: arpancodez
Module: validators.py
==================================================================================
"""

import re
from typing import Union, List

# ==================================================================================
# REGEX PATTERNS
# ==================================================================================
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_PATTERN = r'^[0-9]{10}$'  # Indian phone numbers
PINCODE_PATTERN = r'^[0-9]{6}$'  # Indian pincode
ALPHANUMERIC_PATTERN = r'^[a-zA-Z0-9]+$'

# ==================================================================================
# VALIDATION FUNCTIONS
# ==================================================================================

def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid email format, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    return re.match(EMAIL_PATTERN, email.strip()) is not None


def validate_phone(phone: str) -> bool:
    """
    Validate Indian phone number (10 digits).
    
    Args:
        phone: Phone number to validate
        
    Returns:
        bool: True if valid phone format, False otherwise
    """
    if not phone or not isinstance(phone, str):
        return False
    cleaned = phone.strip().replace('-', '').replace(' ', '')
    return re.match(PHONE_PATTERN, cleaned) is not None


def validate_pincode(pincode: str) -> bool:
    """
    Validate Indian pincode (6 digits).
    
    Args:
        pincode: Pincode to validate
        
    Returns:
        bool: True if valid pincode format, False otherwise
    """
    if not pincode or not isinstance(pincode, str):
        return False
    return re.match(PINCODE_PATTERN, pincode.strip()) is not None


def validate_price(price: Union[int, float], min_price: float = 0.0) -> bool:
    """
    Validate price is a positive number.
    
    Args:
        price: Price value to validate
        min_price: Minimum allowed price (default: 0.0)
        
    Returns:
        bool: True if price is valid, False otherwise
    """
    try:
        price_float = float(price)
        return price_float >= min_price and price_float < 1000000
    except (TypeError, ValueError):
        return False


def validate_quantity(quantity: int, max_qty: int = 1000) -> bool:
    """
    Validate quantity is a positive integer.
    
    Args:
        quantity: Quantity to validate
        max_qty: Maximum allowed quantity
        
    Returns:
        bool: True if quantity is valid, False otherwise
    """
    try:
        qty_int = int(quantity)
        return 1 <= qty_int <= max_qty
    except (TypeError, ValueError):
        return False


def validate_address(address: str, min_length: int = 5, max_length: int = 255) -> bool:
    """
    Validate delivery address format and length.
    
    Args:
        address: Address to validate
        min_length: Minimum address length
        max_length: Maximum address length
        
    Returns:
        bool: True if address is valid, False otherwise
    """
    if not address or not isinstance(address, str):
        return False
    cleaned = address.strip()
    return min_length <= len(cleaned) <= max_length


def validate_string(text: str, min_len: int = 1, max_len: int = 255,
                   allow_special: bool = True) -> bool:
    """
    Generic string validation with length and character checks.
    
    Args:
        text: Text to validate
        min_len: Minimum string length
        max_len: Maximum string length
        allow_special: Whether to allow special characters
        
    Returns:
        bool: True if string is valid, False otherwise
    """
    if not text or not isinstance(text, str):
        return False
    
    cleaned = text.strip()
    if not (min_len <= len(cleaned) <= max_len):
        return False
    
    if not allow_special:
        return cleaned.replace(' ', '').replace('-', '').isalnum()
    
    return True


def validate_restaurant_name(name: str) -> bool:
    """
    Validate restaurant name (3-100 chars, alphanumeric + spaces/hyphens).
    
    Args:
        name: Restaurant name to validate
        
    Returns:
        bool: True if restaurant name is valid
    """
    return validate_string(name, min_len=3, max_len=100, allow_special=True)


def validate_dish_name(name: str) -> bool:
    """
    Validate dish/item name (2-100 chars).
    
    Args:
        name: Dish name to validate
        
    Returns:
        bool: True if dish name is valid
    """
    return validate_string(name, min_len=2, max_len=100)


def validate_order_amount(amount: float) -> bool:
    """
    Validate order total amount (minimum 100 INR).
    
    Args:
        amount: Order amount to validate
        
    Returns:
        bool: True if amount meets minimum order value
    """
    return validate_price(amount, min_price=100.0)


def validate_rating(rating: Union[int, float]) -> bool:
    """
    Validate rating is between 1-5 stars.
    
    Args:
        rating: Rating value to validate
        
    Returns:
        bool: True if rating is 1-5, False otherwise
    """
    try:
        rating_float = float(rating)
        return 1.0 <= rating_float <= 5.0
    except (TypeError, ValueError):
        return False


def validate_batch(items: List[dict], required_keys: List[str]) -> bool:
    """
    Validate a batch of items (orders, menu items, etc).
    
    Args:
        items: List of item dictionaries
        required_keys: List of required keys in each item
        
    Returns:
        bool: True if all items have required keys
    """
    if not isinstance(items, list):
        return False
    
    return all(
        isinstance(item, dict) and all(key in item for key in required_keys)
        for item in items
    )

# ==================================================================================
# END OF VALIDATORS
# ==================================================================================
