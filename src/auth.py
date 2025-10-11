"""
================================================================================
AUTHENTICATION MODULE
================================================================================
This module provides comprehensive authentication and user management services
for the food delivery system, including secure password hashing, input validation,
user authentication, and registration functionality.

Author: arpancodez
Module: auth.py
================================================================================
"""

# ============================================================================
# IMPORTS
# ============================================================================
import hashlib
import re
import logging
from typing import Optional, Dict, Any
from db_manager import DatabaseManager

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTS
# ============================================================================
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 20
MIN_PASSWORD_LENGTH = 6
EMAIL_REGEX_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# ============================================================================
# PASSWORD HASHING FUNCTIONS
# ============================================================================

def hash_password(password: str) -> str:
    """
    Securely hash a password using SHA256 algorithm.
    
    Args:
        password (str): Plain text password to be hashed
        
    Returns:
        str: Hexadecimal string representation of the hashed password
        
    Example:
        >>> hashed = hash_password("mypassword123")
        >>> print(len(hashed))
        64
    """
    try:
        # Encode password to bytes and hash using SHA256
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        logger.debug("Password successfully hashed")
        return password_hash
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise

# ============================================================================
# INPUT VALIDATION FUNCTIONS
# ============================================================================

def validate_email(email: str) -> bool:
    """
    Validate email address format using regex pattern.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
        
    Example:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid-email")
        False
    """
    if not email:
        logger.warning("Email validation failed: Empty email provided")
        return False
        
    # Check email format against regex pattern
    is_valid = re.match(EMAIL_REGEX_PATTERN, email) is not None
    
    if not is_valid:
        logger.warning(f"Email validation failed: Invalid format for {email}")
    
    return is_valid


def validate_username(username: str) -> bool:
    """
    Validate username format and length requirements.
    
    Requirements:
        - Must be alphanumeric (letters and numbers only)
        - Length must be between 3 and 20 characters
        
    Args:
        username (str): Username to validate
        
    Returns:
        bool: True if username meets all requirements, False otherwise
        
    Example:
        >>> validate_username("john123")
        True
        >>> validate_username("ab")
        False
    """
    # Check if username exists and meets length requirements
    if not username:
        logger.warning("Username validation failed: Empty username provided")
        return False
        
    if len(username) < MIN_USERNAME_LENGTH or len(username) > MAX_USERNAME_LENGTH:
        logger.warning(
            f"Username validation failed: Length {len(username)} is outside "
            f"allowed range [{MIN_USERNAME_LENGTH}-{MAX_USERNAME_LENGTH}]"
        )
        return False
    
    # Check if username contains only alphanumeric characters
    if not username.isalnum():
        logger.warning(f"Username validation failed: Non-alphanumeric characters in {username}")
        return False
        
    return True


def validate_password(password: str) -> bool:
    """
    Validate password meets minimum security requirements.
    
    Requirements:
        - Minimum length of 6 characters
        
    Args:
        password (str): Password to validate
        
    Returns:
        bool: True if password meets requirements, False otherwise
        
    Example:
        >>> validate_password("securepass123")
        True
        >>> validate_password("123")
        False
    """
    if not password:
        logger.warning("Password validation failed: Empty password provided")
        return False
        
    is_valid = len(password) >= MIN_PASSWORD_LENGTH
    
    if not is_valid:
        logger.warning(
            f"Password validation failed: Length {len(password)} is below "
            f"minimum requirement of {MIN_PASSWORD_LENGTH}"
        )
    
    return is_valid

# ============================================================================
# USER AUTHENTICATION FUNCTIONS
# ============================================================================

def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user by verifying username and password credentials.
    
    This function performs the following steps:
    1. Validates input parameters
    2. Connects to the database
    3. Retrieves user record by username
    4. Compares hashed password with stored hash
    
    Args:
        username (str): Username to authenticate
        password (str): Plain text password to verify
        
    Returns:
        bool: True if authentication successful, False otherwise
        
    Example:
        >>> success = authenticate_user("john123", "mypassword")
        >>> if success:
        ...     print("Login successful")
    """
    # Validate input parameters
    if not username or not password:
        logger.warning("Authentication failed: Missing username or password")
        return False
    
    # Initialize database connection
    db = DatabaseManager()
    
    if not db.connect():
        logger.error("Authentication failed: Could not connect to database")
        return False
    
    try:
        # Retrieve user record from database
        user = db.get_user_by_username(username)
        
        if not user:
            logger.warning(f"Authentication failed: User '{username}' not found")
            db.disconnect()
            return False
        
        # Hash provided password and compare with stored hash
        password_hash = hash_password(password)
        
        if user.get('password_hash') == password_hash:
            logger.info(f"Authentication successful for user '{username}'")
            db.disconnect()
            return True
        else:
            logger.warning(f"Authentication failed: Invalid password for user '{username}'")
            db.disconnect()
            return False
            
    except Exception as e:
        logger.error(f"Authentication error for user '{username}': {e}")
        db.disconnect()
        return False

# ============================================================================
# USER REGISTRATION FUNCTIONS
# ============================================================================

def register_user(
    username: str,
    email: str,
    password: str,
    phone: str = "",
    address: str = ""
) -> bool:
    """
    Register a new user in the system with comprehensive validation.
    
    This function performs the following operations:
    1. Validates username format and length
    2. Validates email format
    3. Validates password strength
    4. Checks for existing username
    5. Creates user record with hashed password
    
    Args:
        username (str): Desired username (alphanumeric, 3-20 chars)
        email (str): User's email address
        password (str): Plain text password (min 6 chars)
        phone (str, optional): User's phone number. Defaults to "".
        address (str, optional): User's physical address. Defaults to "".
        
    Returns:
        bool: True if registration successful, False otherwise
        
    Example:
        >>> success = register_user(
        ...     username="john123",
        ...     email="john@example.com",
        ...     password="securepass",
        ...     phone="1234567890"
        ... )
    """
    logger.info(f"Registration attempt for username: {username}")
    
    # Validate username format and length
    if not validate_username(username):
        logger.warning(f"Registration failed: Invalid username '{username}'")
        print("Invalid username. Must be alphanumeric, 3-20 characters.")
        return False
    
    # Validate email format
    if not validate_email(email):
        logger.warning(f"Registration failed: Invalid email '{email}'")
        print("Invalid email format.")
        return False
    
    # Validate password strength
    if not validate_password(password):
        logger.warning("Registration failed: Password does not meet requirements")
        print(f"Password must be at least {MIN_PASSWORD_LENGTH} characters long.")
        return False
    
    # Hash the password for secure storage
    try:
        password_hash = hash_password(password)
    except Exception as e:
        logger.error(f"Registration failed: Error hashing password - {e}")
        print("An error occurred during registration. Please try again.")
        return False
    
    # Initialize database connection
    db = DatabaseManager()
    
    if not db.connect():
        logger.error("Registration failed: Could not connect to database")
        print("Could not connect to database.")
        return False
    
    try:
        # Check if username already exists
        existing_user = db.get_user_by_username(username)
        
        if existing_user:
            logger.warning(f"Registration failed: Username '{username}' already exists")
            print("Username already exists. Please choose a different username.")
            db.disconnect()
            return False
        
        # Create new user record in database
        result = db.create_user(username, email, password_hash, phone, address)
        db.disconnect()
        
        if result:
            logger.info(f"Registration successful for user '{username}'")
            print(f"User '{username}' registered successfully!")
            return True
        else:
            logger.error(f"Registration failed: Database error for user '{username}'")
            print("Failed to create user. Please try again.")
            return False
            
    except Exception as e:
        logger.error(f"Registration error for user '{username}': {e}")
        print(f"Registration error: {e}")
        db.disconnect()
        return False

# ============================================================================
# USER INFORMATION RETRIEVAL FUNCTIONS
# ============================================================================

def get_user_info(username: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve complete user information from the database.
    
    Args:
        username (str): Username of the user to retrieve
        
    Returns:
        Optional[Dict[str, Any]]: Dictionary containing user information if found,
                                  None if user not found or error occurred
                                  
    User dictionary structure:
        {
            'user_id': int,
            'username': str,
            'email': str,
            'password_hash': str,
            'phone': str,
            'address': str,
            'created_at': datetime
        }
        
    Example:
        >>> user_info = get_user_info("john123")
        >>> if user_info:
        ...     print(f"Email: {user_info['email']}")
    """
    if not username:
        logger.warning("Get user info failed: Empty username provided")
        return None
    
    # Initialize database connection
    db = DatabaseManager()
    
    if not db.connect():
        logger.error("Get user info failed: Could not connect to database")
        return None
    
    try:
        # Retrieve user information from database
        user = db.get_user_by_username(username)
        db.disconnect()
        
        if user:
            logger.info(f"Successfully retrieved info for user '{username}'")
        else:
            logger.warning(f"User '{username}' not found in database")
            
        return user
        
    except Exception as e:
        logger.error(f"Error getting user info for '{username}': {e}")
        print(f"Error getting user info: {e}")
        db.disconnect()
        return None

# ============================================================================
# END OF MODULE
# ============================================================================
