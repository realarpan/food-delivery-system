import hashlib
import secrets
from typing import Tuple

def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
    """Hash password with salt."""
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return hashed.hex(), salt

def verify_password(password: str, hashed: str, salt: str) -> bool:
    """Verify password against hash."""
    computed_hash, _ = hash_password(password, salt)
    return computed_hash == hashed

def generate_token() -> str:
    """Generate secure random token."""
    return secrets.token_urlsafe(32)

def is_strong_password(password: str) -> bool:
    """Check password strength."""
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password)
