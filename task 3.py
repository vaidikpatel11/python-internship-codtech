import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database connection
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
''')
conn.commit()

# User authentication (simplified)
def authenticate():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "password":
        login_window.destroy()
        main_window()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Main window
def main_window():
    global tree
    global search_entry

    window = tk.Tk()
    window.title("Inventory Management System")

    # Treeview for displaying products
    tree = ttk.Treeview(window, columns=("Name", "Quantity", "Price"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")
    tree.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # Search bar
    search_label = tk.Label(window, text="Search:")
    search_label.grid(row=1, column=0, padx=5, pady=5)
    search_entry = tk.Entry(window)
    search_entry.grid(row=1, column=1, padx=5, pady=5)
    search_button = tk.Button(window, text="Search", command=search_products)
    search_button.grid(row=1, column=2, padx=5, pady=5)

    # Buttons for adding, editing, and deleting
    add_button = tk.Button(window, text="Add Product", command=add_product_window)
    add_button.grid(row=2, column=0, padx=5, pady=5)
    edit_button = tk.Button(window, text="Edit Product", command=edit_product_window)
    edit_button.grid(row=2, column=1, padx=5, pady=5)
    delete_button = tk.Button(window, text="Delete Product", command=delete_product)
    delete_button.grid(row=2, column=2, padx=5, pady=5)

    # Low stock alert (example)
    low_stock_button = tk.Button(window, text="Low Stock Alert", command=low_stock_alert)
    low_stock_button.grid(row=3, column=0, padx=5, pady=5)

    # Load products into Treeview
    load_products()

    window.mainloop()

# Add product window
def add_product_window():
    add_window = tk.Toplevel()
    add_window.title("Add Product")

    name_label = tk.Label(add_window, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    quantity_label = tk.Label(add_window, text="Quantity:")
    quantity_label.grid(row=1, column=0, padx=5, pady=5)
    quantity_entry = tk.Entry(add_window)
    quantity_entry.grid(row=1, column=1, padx=5, pady=5)

    price_label = tk.Label(add_window, text="Price:")
    price_label.grid(row=2, column=0, padx=5, pady=5)
    price_entry = tk.Entry(add_window)
    price_entry.grid(row=2, column=1, padx=5, pady=5)

    def save_product():
        name = name_entry.get()
        quantity = quantity_entry.get()
        price = price_entry.get()

        if not name or not quantity or not price:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for quantity or price.")
            return

        cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
                       (name, quantity, price))
        conn.commit()
        load_products()
        add_window.destroy()

    save_button = tk.Button(add_window, text="Save", command=save_product)
    save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Edit product window
def edit_product_window():
    selected_item = tree.selection()[0]
    item_id = tree.item(selected_item)['values'][0]

    edit_window = tk.Toplevel()
    edit_window.title("Edit Product")

    name_label = tk.Label(edit_window, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(edit_window)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    quantity_label = tk.Label(edit_window, text="Quantity:")
    quantity_label.grid(row=1, column=0, padx=5, pady=5)
    quantity_entry = tk.Entry(edit_window)
    quantity_entry.grid(row=1, column=1, padx=5, pady=5)

    price_label = tk.Label(edit_window, text="Price:")
    price_label.grid(row=2, column=0, padx=5, pady=5)
    price_entry = tk.Entry(edit_window)
    price_entry.grid(row=2, column=1, padx=5, pady=5)

    # Get current values
    cursor.execute("SELECT * FROM products WHERE id=?", (item_id,))
    product = cursor.fetchone()
    name_entry.insert(0, product[1])
    quantity_entry.insert(0, str(product[2]))
    price_entry.insert(0, str(product[3]))

    def update_product():
        name = name_entry.get()
        quantity = quantity_entry.get()
        price = price_entry.get()

        if not name or not quantity or not price:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for quantity or price.")
            return

        cursor.execute("UPDATE products SET name=?, quantity=?, price=? WHERE id=?",
                       (name, quantity, price, item_id))
        conn.commit()
        load_products()
        edit_window.destroy()

    update_button = tk.Button(edit_window, text="Update", command=update_product)
    update_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Delete product
def delete_product():
    selected_item = tree.selection()[0]
    if selected_item:
        item_id = tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            cursor.execute("DELETE FROM products WHERE id=?", (item_id,))
            conn.commit()
            load_products()

# Search products
def search_products():
    search_term = search_entry.get()
    if search_term:
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)

        # Search and display matching products
        cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_term + '%',))
        products = cursor.fetchall()
        for product in products:
            tree.insert("", "end", values=(product[0], product[1], product[2]))

# Low stock alert (example)
def low_stock_alert():
    low_stock_threshold = 10  # Adjust as needed
    cursor.execute