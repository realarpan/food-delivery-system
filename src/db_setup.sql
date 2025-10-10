-- Food Delivery System Database Schema

CREATE DATABASE IF NOT EXISTS food_delivery_db;
USE food_delivery_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Restaurants table
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(20),
    rating DECIMAL(2,1) DEFAULT 0.0,
    cuisine_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Menu items table
CREATE TABLE IF NOT EXISTS menu_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled') DEFAULT 'pending',
    delivery_address TEXT NOT NULL,
    payment_method VARCHAR(50),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_time TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    item_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id) ON DELETE CASCADE
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    order_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

-- Insert sample restaurants
INSERT INTO restaurants (name, address, phone, cuisine_type, rating) VALUES
('Pizza Palace', '123 Main St, City', '555-0101', 'Italian', 4.5),
('Burger Haven', '456 Oak Ave, City', '555-0102', 'American', 4.2),
('Sushi World', '789 Pine Rd, City', '555-0103', 'Japanese', 4.7),
('Pasta Paradise', '321 Elm St, City', '555-0104', 'Italian', 4.3),
('Salad Central', '654 Maple Dr, City', '555-0105', 'Healthy', 4.1);

-- Insert sample menu items
INSERT INTO menu_items (restaurant_id, name, description, price, category) VALUES
(1, 'Margherita Pizza', 'Classic tomato and mozzarella pizza', 12.99, 'Main Course'),
(1, 'Pepperoni Pizza', 'Spicy pepperoni with cheese', 14.99, 'Main Course'),
(2, 'Classic Burger', 'Beef patty with lettuce and tomato', 8.99, 'Main Course'),
(2, 'Cheese Burger', 'Double cheese with special sauce', 10.99, 'Main Course'),
(3, 'California Roll', 'Fresh avocado and crab stick', 9.99, 'Appetizer'),
(3, 'Salmon Sushi', 'Premium salmon nigiri', 15.99, 'Main Course'),
(4, 'Spaghetti Carbonara', 'Creamy pasta with bacon', 10.99, 'Main Course'),
(4, 'Fettuccine Alfredo', 'Rich cream sauce pasta', 11.99, 'Main Course'),
(5, 'Caesar Salad', 'Romaine lettuce with Caesar dressing', 6.99, 'Appetizer'),
(5, 'Greek Salad', 'Fresh vegetables with feta cheese', 7.99, 'Main Course');
