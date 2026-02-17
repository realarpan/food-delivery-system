"""
==================================================================================
CONFIGURATION MODULE
==================================================================================
Centralized configuration settings for the food delivery system including database
connection parameters, API settings, and application constants.

Author: arpancodez
Module: config.py
==================================================================================
"""

import os
from typing import Optional

# ==================================================================================
# DATABASE CONFIGURATION
# ==================================================================================
DB_HOST: str = os.getenv('DB_HOST', 'localhost')
DB_USER: str = os.getenv('DB_USER', 'root')
DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
DB_NAME: str = os.getenv('DB_NAME', 'food_delivery')
DB_PORT: int = int(os.getenv('DB_PORT', '3306'))
DB_CHARSET: str = 'utf8mb4'

# Database connection pool settings
DB_POOL_SIZE: int = 5
DB_POOL_RECYCLE: int = 3600  # Recycle connections after 1 hour
DB_ECHO: bool = False  # Set to True for SQL query logging

# ==================================================================================
# APPLICATION SETTINGS
# ==================================================================================
APP_NAME: str = 'Food Delivery App'
APP_VERSION: str = '1.0.0'
DEBUG_MODE: bool = os.getenv('DEBUG', 'False').lower() == 'true'

# ==================================================================================
# AUTHENTICATION & SECURITY
# ==================================================================================
MIN_USERNAME_LENGTH: int = 3
MAX_USERNAME_LENGTH: int = 20
MIN_PASSWORD_LENGTH: int = 6
MAX_PASSWORD_LENGTH: int = 128
PASSWORD_SALT_ROUNDS: int = 10
SESSION_TIMEOUT_MINUTES: int = 30

# ==================================================================================
# DELIVERY CONFIGURATION
# ==================================================================================
DEFAULT_DELIVERY_FEE: float = 50.0  # In rupees
MIN_ORDER_AMOUNT: float = 100.0
MAX_DELIVERY_DISTANCE_KM: float = 15.0
AVERAGE_DELIVERY_TIME_MINUTES: int = 30
DELIVERY_STATUS_TIMEOUT_MINUTES: int = 120

# ==================================================================================
# PAGINATION SETTINGS
# ==================================================================================
DEFAULT_PAGE_SIZE: int = 20
MAX_PAGE_SIZE: int = 100

# ==================================================================================
# API RATE LIMITING
# ==================================================================================
RATE_LIMIT_ENABLED: bool = True
RATE_LIMIT_REQUESTS: int = 100
RATE_LIMIT_WINDOW_SECONDS: int = 60

# ==================================================================================
# LOGGING CONFIGURATION
# ==================================================================================
LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE: str = 'logs/app.log'
LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_MAX_BYTES: int = 10485760  # 10MB
LOG_BACKUP_COUNT: int = 5

# ==================================================================================
# CACHE SETTINGS
# ==================================================================================
CACHE_ENABLED: bool = True
CACHE_TTL_SECONDS: int = 300  # 5 minutes

# ==================================================================================
# EMAIL CONFIGURATION
# ==================================================================================
SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME: str = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD', '')
SMTP_FROM_EMAIL: str = os.getenv('SMTP_FROM_EMAIL', 'noreply@fooddelivery.com')
SEND_EMAIL_ENABLED: bool = os.getenv('SEND_EMAIL_ENABLED', 'False').lower() == 'true'

# ==================================================================================
# NOTIFICATION SETTINGS
# ==================================================================================
SMS_ENABLED: bool = False
PUSH_NOTIFICATION_ENABLED: bool = False
WEBHOOK_TIMEOUT_SECONDS: int = 10

# ==================================================================================
# FILE UPLOAD SETTINGS
# ==================================================================================
UPLOAD_FOLDER: str = 'uploads'
MAX_FILE_SIZE_MB: int = 10
ALLOWED_EXTENSIONS: tuple = ('jpg', 'jpeg', 'png', 'gif', 'pdf')

# ==================================================================================
# TIMEZONE & LOCALE
# ==================================================================================
TIMEZONE: str = 'Asia/Kolkata'
DEFAULT_LOCALE: str = 'en_IN'
CURRENCY: str = 'USD'

# ==================================================================================
# END OF CONFIGURATION
# ==================================================================================
