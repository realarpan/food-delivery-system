import tkinter as tk
from tkinter import messagebox, ttk
import db_manager
import auth

class FoodDeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Delivery System")
        self.root.geometry("800x600")
        self.current_user = None
        self.show_login_screen()
    
    def show_login_screen(self):
        self.clear_window()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Food Delivery System", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(frame, text="Username:").pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.pack(pady=5)
        
        tk.Label(frame, text="Password:").pack()
        self.password_entry = tk.Entry(frame, width=30, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(frame, text="Login", command=self.login, width=20).pack(pady=10)
        tk.Button(frame, text="Sign Up", command=self.show_signup_screen, width=20).pack()
    
    def show_signup_screen(self):
        self.clear_window()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Create Account", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(frame, text="Username:").pack()
        self.new_username_entry = tk.Entry(frame, width=30)
        self.new_username_entry.pack(pady=5)
        
        tk.Label(frame, text="Email:").pack()
        self.new_email_entry = tk.Entry(frame, width=30)
        self.new_email_entry.pack(pady=5)
        
        tk.Label(frame, text="Password:").pack()
        self.new_password_entry = tk.Entry(frame, width=30, show="*")
        self.new_password_entry.pack(pady=5)
        
        tk.Button(frame, text="Register", command=self.register, width=20).pack(pady=10)
        tk.Button(frame, text="Back to Login", command=self.show_login_screen, width=20).pack()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if auth.authenticate_user(username, password):
            self.current_user = username
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def register(self):
        username = self.new_username_entry.get()
        email = self.new_email_entry.get()
        password = self.new_password_entry.get()
        
        if auth.register_user(username, email, password):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "Registration failed")
    
    def show_main_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        
        tk.Label(frame, text=f"Welcome, {self.current_user}!", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Button(frame, text="Browse Menu", command=self.show_menu, width=25, height=2).pack(pady=10)
        tk.Button(frame, text="View Orders", command=self.show_orders, width=25, height=2).pack(pady=10)
        tk.Button(frame, text="Logout", command=self.logout, width=25, height=2).pack(pady=10)
    
    def show_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Restaurant Menu", font=("Arial", 18, "bold")).pack(pady=10)
        
        menu_frame = tk.Frame(frame)
        menu_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(menu_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.menu_listbox = tk.Listbox(menu_frame, yscrollcommand=scrollbar.set, height=15)
        self.menu_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.menu_listbox.yview)
        
        # Sample menu items
        menu_items = [
            "Pizza - $12.99",
            "Burger - $8.99",
            "Pasta - $10.99",
            "Salad - $6.99",
            "Sushi - $15.99"
        ]
        for item in menu_items:
            self.menu_listbox.insert(tk.END, item)
        
        tk.Button(frame, text="Place Order", command=self.place_order, width=20).pack(pady=10)
        tk.Button(frame, text="Back", command=self.show_main_menu, width=20).pack()
    
    def place_order(self):
        selection = self.menu_listbox.curselection()
        if selection:
            item = self.menu_listbox.get(selection[0])
            messagebox.showinfo("Order Placed", f"Your order for {item} has been placed!")
        else:
            messagebox.showwarning("Warning", "Please select an item")
    
    def show_orders(self):
        self.clear_window()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Your Orders", font=("Arial", 18, "bold")).pack(pady=10)
        
        orders_text = tk.Text(frame, height=15, width=60)
        orders_text.pack(pady=10)
        orders_text.insert(tk.END, "No orders yet.")
        orders_text.config(state=tk.DISABLED)
        
        tk.Button(frame, text="Back", command=self.show_main_menu, width=20).pack(pady=10)
    
    def logout(self):
        self.current_user = None
        self.show_login_screen()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodDeliveryApp(root)
    root.mainloop()
