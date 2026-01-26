from typing import Any, Dict, Optional
from datetime import datetime

def success_response(data: Any = None, message: str = "Success", code: int = 200) -> Dict:
    """Format successful API response."""
    return {
        "status": "success",
        "code": code,
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }

def error_response(message: str, code: int = 400, error_code: str = None) -> Dict:
    """Format error API response."""
    return {
        "status": "error",
        "code": code,
        "error_code": error_code,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }

def paginated_response(items: list, total: int, page: int, per_page: int) -> Dict:
    """Format paginated response."""
    return {
        "status": "success",
        "data": items,
        "pagination": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page
        },
        "timestamp": datetime.now().isoformat()
    }
