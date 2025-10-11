"""
================================================================================
TKINTER UI MODULE
================================================================================
Professional, consistent Tkinter UI for the Food Delivery System with clear
structure, comments, input validation, and better error handling.

Author: arpancodez
Module: tkinter_ui.py
================================================================================
"""

# ============================================================================
# IMPORTS
# ============================================================================
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Dict, Any

from db_manager import DatabaseManager
import auth

# ============================================================================
# UI CONSTANTS
# ============================================================================
APP_TITLE = "Food Delivery System"
WINDOW_SIZE = "900x650"
FONT_H1 = ("Arial", 22, "bold")
FONT_H2 = ("Arial", 18, "bold")
FONT_BODY = ("Arial", 12)
PADDING = {"padx": 16, "pady": 16}


# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================
class FoodDeliveryApp:
    """Main Tkinter application for the Food Delivery System."""

    def __init__(self, root: tk.Tk) -> None:
        # Window config
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)

        # State
        self.current_user: str | None = None
        self.db = DatabaseManager()
        self.cart: List[Dict[str, Any]] = []
        self.selected_restaurant_id: int | None = None

        # Initial screen
        self.show_login_screen()

    # ------------------------------------------------------------------
    # UTILITY METHODS
    # ------------------------------------------------------------------
    def clear_window(self) -> None:
        """Remove all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def require_db(self) -> bool:
        """Ensure DB connection is available and show an error if not."""
        if not self.db.connect():
            messagebox.showerror("Database", "Could not connect to database. Configure DB credentials.")
            return False
        return True

    # ------------------------------------------------------------------
    # AUTH SCREENS
    # ------------------------------------------------------------------
    def show_login_screen(self) -> None:
        """Render the login UI."""
        self.clear_window()
        frame = tk.Frame(self.root, padx=24, pady=24)
        frame.pack(expand=True)

        tk.Label(frame, text=APP_TITLE, font=("Arial", 26, "bold")).pack(pady=10)

        form = tk.Frame(frame)
        form.pack(pady=10)
        tk.Label(form, text="Username:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.username_entry = tk.Entry(form, width=30)
        self.username_entry.grid(row=0, column=1)

        tk.Label(form, text="Password:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.password_entry = tk.Entry(form, width=30, show="*")
        self.password_entry.grid(row=1, column=1)

        actions = tk.Frame(frame)
        actions.pack(pady=10)
        tk.Button(actions, text="Login", width=18, command=self.login).grid(row=0, column=0, padx=5)
        tk.Button(actions, text="Sign Up", width=18, command=self.show_signup_screen).grid(row=0, column=1, padx=5)

    def show_signup_screen(self) -> None:
        """Render the sign-up UI."""
        self.clear_window()
        frame = tk.Frame(self.root, padx=24, pady=24)
        frame.pack(expand=True)

        tk.Label(frame, text="Create Account", font=FONT_H1).pack(pady=10)

        form = tk.Frame(frame)
        form.pack(pady=10)
        tk.Label(form, text="Username:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.new_username_entry = tk.Entry(form, width=30)
        self.new_username_entry.grid(row=0, column=1)

        tk.Label(form, text="Email:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.new_email_entry = tk.Entry(form, width=30)
        self.new_email_entry.grid(row=1, column=1)

        tk.Label(form, text="Password:").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        self.new_password_entry = tk.Entry(form, width=30, show="*")
        self.new_password_entry.grid(row=2, column=1)

        tk.Label(form, text="Phone (optional):").grid(row=3, column=0, sticky="e", padx=6, pady=6)
        self.new_phone_entry = tk.Entry(form, width=30)
        self.new_phone_entry.grid(row=3, column=1)

        tk.Label(form, text="Address (optional):").grid(row=4, column=0, sticky="e", padx=6, pady=6)
        self.new_address_entry = tk.Entry(form, width=30)
        self.new_address_entry.grid(row=4, column=1)

        actions = tk.Frame(frame)
        actions.pack(pady=10)
        tk.Button(actions, text="Register", width=18, command=self.register).grid(row=0, column=0, padx=5)
        tk.Button(actions, text="Back to Login", width=18, command=self.show_login_screen).grid(row=0, column=1, padx=5)

    # ------------------------------------------------------------------
    # AUTH LOGIC
    # ------------------------------------------------------------------
    def login(self) -> None:
        """Handle login button press with input validation."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Login", "Please enter username and password")
            return
        ok = auth.authenticate_user(username, password)
        if ok:
            self.current_user = username
            self.show_main_menu()
        else:
            messagebox.showerror("Login", "Invalid credentials")

    def register(self) -> None:
        """Handle registration with validation and feedback."""
        username = self.new_username_entry.get().strip()
        email = self.new_email_entry.get().strip()
        password = self.new_password_entry.get().strip()
        phone = self.new_phone_entry.get().strip() or None
        address = self.new_address_entry.get().strip() or None

        ok = auth.register_user(username, email, password, phone, address)
        if ok:
            messagebox.showinfo("Register", "Registration successful! Please login.")
            self.show_login_screen()
        else:
            messagebox.showerror("Register", "Registration failed. Check input and try again.")

    def logout(self) -> None:
        """Clear session and return to login."""
        self.current_user = None
        self.cart.clear()
        self.selected_restaurant_id = None
        self.show_login_screen()

    # ------------------------------------------------------------------
    # MAIN MENU
    # ------------------------------------------------------------------
    def show_main_menu(self) -> None:
        self.clear_window()
        container = tk.Frame(self.root, **PADDING)
        container.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(container)
        header.pack(fill=tk.X)
        tk.Label(header, text=f"Welcome, {self.current_user}!", font=FONT_H2).pack(side=tk.LEFT)
        tk.Button(header, text="Logout", command=self.logout).pack(side=tk.RIGHT)

        actions = tk.Frame(container)
        actions.pack(pady=12)
        tk.Button(actions, text="Browse Restaurants", width=22, height=2, command=self.show_restaurants).grid(row=0, column=0, padx=8, pady=8)
        tk.Button(actions, text="View Cart", width=22, height=2, command=self.show_cart).grid(row=0, column=1, padx=8, pady=8)
        tk.Button(actions, text="Your Orders", width=22, height=2, command=self.show_orders).grid(row=0, column=2, padx=8, pady=8)

    # ------------------------------------------------------------------
    # RESTAURANTS AND MENU
    # ------------------------------------------------------------------
    def show_restaurants(self) -> None:
        if not self.require_db():
            return
        if not hasattr(self.db, 'get_restaurants'):
            messagebox.showerror("Feature", "Backend method get_restaurants is missing.")
            return
        restaurants = self.db.get_restaurants() or []
        self.db.disconnect()

        self.clear_window()
        container = tk.Frame(self.root, **PADDING)
        container.pack(fill=tk.BOTH, expand=True)
        tk.Label(container, text="Select a Restaurant", font=FONT_H2).pack(pady=8)

        cols = ("ID", "Name", "Cuisine", "Rating")
        tree = ttk.Treeview(container, columns=cols, show="headings", height=12)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=180 if c == "Name" else 110, anchor="center")
        for r in restaurants:
            tree.insert("", tk.END, values=(r.get("restaurant_id"), r.get("name"), r.get("cuisine_type", "-"), r.get("rating", 0)))
        tree.pack(fill=tk.BOTH, expand=True, pady=8)

        def on_select():
            sel = tree.focus()
            if not sel:
                messagebox.showinfo("Restaurants", "Please select a restaurant")
                return
            vals = tree.item(sel, "values")
            self.selected_restaurant_id = int(vals[0])
            self.show_menu()

        bottom = tk.Frame(container)
        bottom.pack(fill=tk.X)
        tk.Button(bottom, text="Back", command=self.show_main_menu).pack(side=tk.LEFT, pady=6)
        tk.Button(bottom, text="View Menu", command=on_select).pack(side=tk.RIGHT, pady=6)

    def show_menu(self) -> None:
        if not self.selected_restaurant_id:
            messagebox.showwarning("Menu", "Select a restaurant first")
            self.show_restaurants()
            return
        if not self.require_db():
            return
        if not hasattr(self.db, 'get_menu_items'):
            messagebox.showerror("Feature", "Backend method get_menu_items is missing.")
            return
        items = self.db.get_menu_items(self.selected_restaurant_id) or []
        self.db.disconnect()

        self.clear_window()
        container = tk.Frame(self.root, **PADDING)
        container.pack(fill=tk.BOTH, expand=True)

        top = tk.Frame(container)
        top.pack(fill=tk.X)
        tk.Label(top, text="Menu", font=("Arial", 20, "bold")).pack(side=tk.LEFT)
        tk.Button(top, text="Restaurants", command=self.show_restaurants).pack(side=tk.RIGHT, padx=5)
        tk.Button(top, text=f"Cart ({sum(i['qty'] for i in self.cart)} items)", command=self.show_cart).pack(side=tk.RIGHT)

        columns = ("Item ID", "Name", "Category", "Price")
        tree = ttk.Treeview(container, columns=columns, show="headings", height=14)
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=200 if c == "Name" else 120, anchor="center")
        for it in items:
            if it.get("is_available", True):
                tree.insert("", tk.END, values=(it.get("item_id"), it.get("name"), it.get("category", "-"), f"${float(it.get('price', 0)):.2f}"))
        tree.pack(fill=tk.BOTH, expand=True)

        qty_var = tk.IntVar(value=1)
        controls = tk.Frame(container)
        controls.pack(fill=tk.X, pady=8)
        tk.Label(controls, text="Quantity:").pack(side=tk.LEFT)
        qty_spin = tk.Spinbox(controls, from_=1, to=20, textvariable=qty_var, width=5)
        qty_spin.pack(side=tk.LEFT, padx=6)

        def add_to_cart():
            sel = tree.focus()
            if not sel:
                messagebox.showinfo("Menu", "Select an item to add")
                return
            vals = tree.item(sel, "values")
            item_id = int(vals[0])
            name = vals[1]
            price = float(str(vals[3]).replace("$", ""))
            qty = int(qty_var.get())

            # Merge items by item_id
            for it in self.cart:
                if it['item_id'] == item_id:
                    it['qty'] += qty
                    break
            else:
                self.cart.append({'item_id': item_id, 'name': name, 'price': price, 'qty': qty, 'restaurant_id': self.selected_restaurant_id})

            messagebox.showinfo("Cart", f"Added {qty} x {name} to cart")
            self.show_menu()

        tk.Button(controls, text="Add to Cart", command=add_to_cart).pack(side=tk.LEFT, padx=8)
        tk.Button(controls, text="Back", command=self.show_restaurants).pack(side=tk.LEFT)

    # ------------------------------------------------------------------
    # CART
    # ------------------------------------------------------------------
    def show_cart(self) -> None:
        self.clear_window()
        container = tk.Frame(self.root, **PADDING)
        container.pack(fill=tk.BOTH, expand=True)

        tk.Label(container, text="Your Cart", font=("Arial", 20, "bold")).pack(pady=6)

        columns = ("Name", "Qty", "Price", "Subtotal")
        tree = ttk.Treeview(container, columns=columns, show="headings", height=12)
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=180)

        total = 0.0
        for it in self.cart:
            subtotal = it['qty'] * it['price']
            total += subtotal
            tree.insert("", tk.END, values=(it['name'], it['qty'], f"${it['price']:.2f}", f"${subtotal:.2f}"))
        tree.pack(fill=tk.BOTH, expand=True)

        summary = tk.Frame(container)
        summary.pack(fill=tk.X, pady=8)
        tk.Label(summary, text=f"Total: ${total:.2f}", font=("Arial", 14, "bold")).pack(side=tk.LEFT)

        def remove_selected():
            sel = tree.focus()
            if not sel:
                return
            values = tree.item(sel, "values")
            name = values[0]
            for i, it in enumerate(self.cart):
                if it['name'] == name:
                    del self.cart[i]
                    break
            self.show_cart()

        def clear_cart():
            self.cart.clear()
            self.show_cart()

        def checkout():
            # Preconditions
            if not self.current_user:
                messagebox.showwarning("Checkout", "Please login again.")
                return
            if not self.cart:
                messagebox.showinfo("Checkout", "Cart is empty")
                return
            if not self.require_db():
                return

            user = self.db.get_user_by_username(self.current_user)
            if not user:
                self.db.disconnect()
                messagebox.showerror("Checkout", "User not found")
                return

            user_id = user['user_id']
            restaurant_id = self.cart[0]['restaurant_id']
            # Ensure all items from same restaurant
            if any(it['restaurant_id'] != restaurant_id for it in self.cart):
                self.db.disconnect()
                messagebox.showerror("Checkout", "All items must be from the same restaurant")
                return

            total_amount = sum(it['qty'] * it['price'] for it in self.cart)
            address = user.get('address') or 'N/A'
            items_payload = [
                {'item_id': it['item_id'], 'quantity': it['qty'], 'price': it['price']}
                for it in self.cart
            ]

            order_id = self.db.create_order(
                user_id,
                restaurant_id,
                items_payload,
                total_amount,
                address,
                payment_method='cash',
            )
            self.db.disconnect()

            if order_id:
                messagebox.showinfo("Order", f"Order #{order_id} placed successfully!")
                self.cart.clear()
                self
