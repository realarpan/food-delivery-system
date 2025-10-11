import mysql.connector
from mysql.connector import Error
import os

class DatabaseManager:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'food_delivery_db')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                cursor.close()
                return results
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Error as e:
            print(f"Error executing query: {e}")
            return None
    
    def get_restaurants(self):
        """Get all active restaurants"""
        query = "SELECT * FROM restaurants WHERE is_active = TRUE ORDER BY rating DESC"
        return self.execute_query(query)
    
    def get_menu_items(self, restaurant_id=None):
        """Get menu items for a restaurant or all items"""
        if restaurant_id:
            query = """SELECT mi.*, r.name as restaurant_name 
                      FROM menu_items mi 
                      JOIN restaurants r ON mi.restaurant_id = r.restaurant_id 
                      WHERE mi.restaurant_id = %s AND mi.is_available = TRUE"""
            return self.execute_query(query, (restaurant_id,))
        else:
            query = """SELECT mi.*, r.name as restaurant_name 
                      FROM menu_items mi 
                      JOIN restaurants r ON mi.restaurant_id = r.restaurant_id 
                      WHERE mi.is_available = TRUE"""
            return self.execute_query(query)
    
    def create_order(self, user_id, restaurant_id, items, total_amount, delivery_address, payment_method='cash'):
        """Create a new order with order items"""
        try:
            # Insert order
            order_query = """INSERT INTO orders 
                           (user_id, restaurant_id, total_amount, delivery_address, payment_method) 
                           VALUES (%s, %s, %s, %s, %s)"""
            cursor = self.connection.cursor()
            cursor.execute(order_query, (user_id, restaurant_id, total_amount, delivery_address, payment_method))
            order_id = cursor.lastrowid
            
            # Insert order items
            items_query = """INSERT INTO order_items 
                           (order_id, item_id, quantity, item_price) 
                           VALUES (%s, %s, %s, %s)"""
            for item in items:
                cursor.execute(items_query, (order_id, item['item_id'], item['quantity'], item['price']))
            
            self.connection.commit()
            cursor.close()
            return order_id
        except Error as e:
            print(f"Error creating order: {e}")
            return None
    
    def get_user_orders(self, user_id):
        """Get all orders for a user"""
        query = """SELECT o.*, r.name as restaurant_name 
                  FROM orders o 
                  JOIN restaurants r ON o.restaurant_id = r.restaurant_id 
                  WHERE o.user_id = %s 
                  ORDER BY o.order_date DESC"""
        return self.execute_query(query, (user_id,))
    
    def get_order_items(self, order_id):
        """Get all items for an order"""
        query = """SELECT oi.*, mi.name as item_name 
                  FROM order_items oi 
                  JOIN menu_items mi ON oi.item_id = mi.item_id 
                  WHERE oi.order_id = %s"""
        return self.execute_query(query, (order_id,))
    
    def get_user_by_username(self, username):
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = %s"
        results = self.execute_query(query, (username,))
        return results[0] if results else None
    
    def create_user(self, username, email, password_hash, phone=None, address=None):
        """Create a new user"""
        query = """INSERT INTO users (username, email, password_hash, phone, address) 
                  VALUES (%s, %s, %s, %s, %s)"""
        return self.execute_query(query, (username, email, password_hash, phone, address))
