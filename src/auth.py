import hashlib
import re
from db_manager import DatabaseManager

def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username (alphanumeric, 3-20 characters)"""
    if not username or len(username) < 3 or len(username) > 20:
        return False
    return username.isalnum()

def validate_password(password):
    """Validate password strength (min 6 characters)"""
    return len(password) >= 6

def authenticate_user(username, password):
    """Authenticate user with username and password"""
    if not username or not password:
        return False
    
    db = DatabaseManager()
    if not db.connect():
        return False
    
    try:
        user = db.get_user_by_username(username)
        if not user:
            db.disconnect()
            return False
        
        # Hash the provided password and compare
        password_hash = hash_password(password)
        if user['password_hash'] == password_hash:
            db.disconnect()
            return True
        else:
            db.disconnect()
            return False
    except Exception as e:
        print(f"Authentication error: {e}")
        db.disconnect()
        return False

def register_user(username, email, password, phone=None, address=None):
    """Register a new user"""
    # Validate inputs
    if not validate_username(username):
        print("Invalid username. Must be alphanumeric, 3-20 characters.")
        return False
    
    if not validate_email(email):
        print("Invalid email format.")
        return False
    
    if not validate_password(password):
        print("Password must be at least 6 characters long.")
        return False
    
    # Hash password
    password_hash = hash_password(password)
    
    # Connect to database
    db = DatabaseManager()
    if not db.connect():
        print("Could not connect to database.")
        return False
    
    try:
        # Check if username already exists
        existing_user = db.get_user_by_username(username)
        if existing_user:
            print("Username already exists.")
            db.disconnect()
            return False
        
        # Create user
        result = db.create_user(username, email, password_hash, phone, address)
        db.disconnect()
        
        if result:
            return True
        else:
            print("Failed to create user.")
            return False
    except Exception as e:
        print(f"Registration error: {e}")
        db.disconnect()
        return False

def get_user_info(username):
    """Get user information by username"""
    db = DatabaseManager()
    if not db.connect():
        return None
    
    try:
        user = db.get_user_by_username(username)
        db.disconnect()
        return user
    except Exception as e:
        print(f"Error getting user info: {e}")
        db.disconnect()
        return None
