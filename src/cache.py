import time
from typing import Any, Optional, Dict
from config import CACHE_TTL_SECONDS

class Cache:
    """Simple in-memory cache with TTL support."""
    def __init__(self, ttl_seconds: int = CACHE_TTL_SECONDS):
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, tuple] = {}
    
    def set(self, key: str, value: Any) -> None:
        """Store value with timestamp."""
        self._cache[key] = (value, time.time())
    
    def get(self, key: str) -> Optional[Any]:
        """Get value if exists and not expired."""
        if key not in self._cache:
            return None
        
        value, timestamp = self._cache[key]
        if time.time() - timestamp > self.ttl_seconds:
            del self._cache[key]
            return None
        return value
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cache."""
        self._cache.clear()
    
    def exists(self, key: str) -> bool:
        """Check if key exists and is valid."""
        return self.get(key) is not None

_global_cache = Cache()

def cache_get(key: str) -> Optional[Any]:
    return _global_cache.get(key)

def cache_set(key: str, value: Any) -> None:
    _global_cache.set(key, value)

def cache_delete(key: str) -> bool:
    return _global_cache.delete(key)
