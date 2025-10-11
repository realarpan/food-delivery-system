"""
================================================================================
DATABASE MANAGEMENT MODULE
================================================================================
This module encapsulates all database interactions for the food delivery system,
including connection management, query execution, and domain-specific operations
such as users and orders management.

Author: arpancodez
Module: db_manager.py
================================================================================
"""

# ============================================================================
# IMPORTS
# ============================================================================
import os
import logging
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import mysql.connector
from mysql.connector import Error, MySQLConnection

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# TYPE ALIASES
# ============================================================================
Params = Optional[Union[Tuple[Any, ...], List[Any]]]
Row = Dict[str, Any]
Rows = List[Row]

# ============================================================================
# DATABASE MANAGER CLASS
# ============================================================================

class DatabaseManager:
    """
    Provides a high-level interface for MySQL database interactions.

    Responsibilities:
    - Manage connection lifecycle (connect/disconnect)
    - Execute parameterized queries with safe defaults
    - Provide helper methods for application-specific operations
    """

    def __init__(self) -> None:
        # Connection configuration via environment variables with sensible defaults
        self.host: str = os.getenv('DB_HOST', 'localhost')
        self.database: str = os.getenv('DB_NAME', 'food_delivery_db')
        self.user: str = os.getenv('DB_USER', 'root')
        self.password: str = os.getenv('DB_PASSWORD', '')
        self.connection: Optional[MySQLConnection] = None

    # ---------------------------------------------------------------------
    # CONNECTION METHODS
    # ---------------------------------------------------------------------
    def connect(self) -> bool:
        """
        Establish a database connection.

        Returns:
            bool: True if successfully connected; otherwise False.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            if self.connection.is_connected():
                logger.info("Database connection established")
                return True
            logger.error("Database connection failed without exception")
            return False
        except Error as e:
            logger.error(f"Error connecting to database: {e}")
            return False

    def disconnect(self) -> None:
        """Close the database connection if it is open."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")

    # ---------------------------------------------------------------------
    # LOW-LEVEL QUERY EXECUTION
    # ---------------------------------------------------------------------
    def execute_query(self, query: str, params: Params = None) -> Union[Rows, bool, None]:
        """
        Execute a SQL query with optional parameters.

        Behavior:
        - SELECT queries return a list of rows (list[dict])
        - Non-SELECT queries return True on success
        - Returns None on error

        Args:
            query (str): SQL query to execute
            params (tuple | list | None): Parameters for the query

        Returns:
            list[dict] | bool | None: Result set for SELECT, True for write, or None on failure
        """
        if not self.connection or not self.connection.is_connected():
            logger.error("execute_query called without an active database connection")
            return None

        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                results: Rows = cursor.fetchall()
                return results
            else:
                self.connection.commit()
                return True
        except Error as e:
            logger.error(f"Error executing query: {e} | Query: {query} | Params: {params}")
            return None
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

    # ---------------------------------------------------------------------
    # USER OPERATIONS
    # ---------------------------------------------------------------------
    def get_user_by_username(self, username: str) -> Optional[Row]:
        """Retrieve a single user row by username."""
        query = "SELECT * FROM users WHERE username = %s"
        results = self.execute_query(query, (username,))
        return results[0] if isinstance(results, list) and results else None

    def create_user(
        self,
        username: str,
        email: str,
        password_hash: str,
        phone: Optional[str] = None,
        address: Optional[str] = None,
    ) -> bool:
        """Insert a new user record into the users table."""
        query = (
            """
            INSERT INTO users (username, email, password_hash, phone, address)
            VALUES (%s, %s, %s, %s, %s)
            """
        )
        result = self.execute_query(query, (username, email, password_hash, phone, address))
        return bool(result)

    # ---------------------------------------------------------------------
    # ORDER OPERATIONS
    # ---------------------------------------------------------------------
    def create_order(
        self,
        user_id: int,
        restaurant_id: int,
        items: Iterable[Dict[str, Any]],
        total_amount: float,
        delivery_address: str,
        payment_method: str = 'cash',
    ) -> Optional[int]:
        """
        Create a new order and corresponding order_items in a single transaction.

        Args:
            user_id (int): ID of the user placing the order
            restaurant_id (int): ID of the restaurant
            items (Iterable[dict]): Collection of items with keys: item_id, quantity, price
            total_amount (float): Total order amount
            delivery_address (str): Address for delivery
            payment_method (str): Payment method, default 'cash'

        Returns:
            Optional[int]: Newly created order ID on success, else None
        """
        if not self.connection or not self.connection.is_connected():
            logger.error("create_order called without an active database connection")
            return None

        cursor = None
        try:
            cursor = self.connection.cursor()
            # Insert into orders table
            order_query = (
                """
                INSERT INTO orders (user_id, restaurant_id, total_amount, delivery_address, payment_method)
                VALUES (%s, %s, %s, %s, %s)
                """
            )
            cursor.execute(order_query, (user_id, restaurant_id, total_amount, delivery_address, payment_method))
            order_id = cursor.lastrowid

            # Insert order items
            items_query = (
                """
                INSERT INTO order_items (order_id, item_id, quantity, item_price)
                VALUES (%s, %s, %s, %s)
                """
            )
            for item in items:
                cursor.execute(
                    items_query,
                    (
                        order_id,
                        int(item['item_id']),
                        int(item['quantity']),
                        float(item['price']),
                    ),
                )

            # Commit transaction
            self.connection.commit()
            return int(order_id)
        except Error as e:
            logger.error(f"Error creating order: {e}")
            try:
                self.connection.rollback()
            except Exception:
                pass
            return None
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

    def get_user_orders(self, user_id: int) -> Optional[Rows]:
        """Return all orders for a user with restaurant name, newest first."""
        query = (
            """
            SELECT o.*, r.name as restaurant_name
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.restaurant_id
            WHERE o.user_id = %s
            ORDER BY o.order_date DESC
            """
        )
        results = self.execute_query(query, (user_id,))
        return results if isinstance(results, list) else None

    def get_order_items(self, order_id: int) -> Optional[Rows]:
        """Return all items for a specific order with menu item name."""
        query = (
            """
            SELECT oi.*, mi.name as item_name
            FROM order_items oi
            JOIN menu_items mi ON oi.item_id = mi.item_id
            WHERE oi.order_id = %s
            """
        )
        results = self.execute_query(query, (order_id,))
        return results if isinstance(results, list) else None

# ============================================================================
# END OF MODULE
# ============================================================================
