import sqlite3
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import config  # Import the config file

print("Starting the application...")

# Define the database path using config
db_path = config.DB_PATH
print(f"Database path: {db_path}")

# Function to register a new user
def register_user(username, password, role):
    if not username or not password or not role:
        messagebox.showerror("Error", "All fields are required.")
        return
    if len(password) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters long.")
        return
    if role not in ["admin", "user"]:
        messagebox.showerror("Error", "Role must be either 'admin' or 'user'.")
        return
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"User {username} registered successfully!")
        print(f"User registered: {username}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to login a user
def login_user(username, password):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = c.fetchone()
        conn.close()
        print(f"User login attempt: {username} - {'Success' if user else 'Failed'}")
        return user
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

# Function to add a new account
def add_account(name, balance):
    if not name or not balance:
        messagebox.showerror("Error", "All fields are required.")
        return
    try:
        balance = float(balance)
    except ValueError:
        messagebox.showerror("Error", "Balance must be a valid number.")
        return
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('INSERT INTO accounts (name, balance) VALUES (?, ?)', (name, balance))
        conn.commit()
        conn.close()
        print(f"Account added: {name}, Balance: {balance}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to view accounts
def view_accounts():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM accounts')
        accounts = c.fetchall()
        conn.close()
        print(f"Accounts viewed: {accounts}")
        return accounts
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return []

# Function to validate inventory input
def validate_inventory_input(item_name, quantity, price):
    if not item_name or not quantity or not price:
        messagebox.showerror("Error", "All fields are required.")
        return False
    try:
        quantity = int(quantity)
        price = float(price)
        return True
    except ValueError:
        messagebox.showerror("Error", "Quantity must be an integer and price must be a valid number.")
        return False

# Function to add a new inventory item
def add_inventory_item(item_name, quantity, price):
    if validate_inventory_input(item_name, quantity, price):
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute('INSERT INTO inventory (item_name, quantity, price) VALUES (?, ?, ?)', (item_name, quantity, price))
            conn.commit()
            conn.close()
            print(f"Inventory item added: {item_name}, Quantity: {quantity}, Price: {price}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Function to view inventory
def view_inventory():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM inventory')
        inventory = c.fetchall()
        conn.close()
        print(f"Inventory viewed: {inventory}")
        return inventory
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return []

# Function to record a sale
def record_sale(item_id, quantity, date):
    if not item_id or not quantity or not date:
        messagebox.showerror("Error", "All fields are required.")
        return
    try:
        item_id = int(item_id)
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Error", "Item ID and quantity must be valid numbers.")
        return
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('INSERT INTO sales (item_id, quantity, date) VALUES (?, ?, ?)', (item_id, quantity, date))
        conn.commit()
        conn.close()
        print(f"Sale recorded: Item ID: {item_id}, Quantity: {quantity}, Date: {date}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to view sales
def view_sales():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM sales')
        sales = c.fetchall()
        conn.close()
        print(f"Sales viewed: {sales}")
        return sales
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return []

# Function to open the main application window
def open_main_application():
    print("Opening the main application window...")
    main_app = Tk()
    main_app.title("TK MNGMNT - Main Application")

    # Create tabs
    tab_control = ttk.Notebook(main_app)
    tab_accounts = ttk.Frame(tab_control)
    tab_inventory = ttk.Frame(tab_control)
    tab_sales = ttk.Frame(tab_control)
    tab_control.add(tab_accounts, text='Accounts')
    tab_control.add(tab_inventory, text='Inventory')
    tab_control.add(tab_sales, text='Sales')
    tab_control.pack(expand=1, fill='both')

    # Accounts Tab
    Label(tab_accounts, text="Accounts Management").grid(row=0, column=0, padx=10, pady=10)

    account_tree = ttk.Treeview(tab_accounts, columns=("ID", "Name", "Balance"), show='headings')
    account_tree.heading("ID", text="ID")
    account_tree.heading("Name", text="Name")
    account_tree.heading("Balance", text="Balance")
    account_tree.grid(row=1, column=0, padx=10, pady=10)

    Button(tab_accounts, text="View Accounts", command=lambda: populate_treeview(account_tree, view_accounts())).grid(row=2, column=0, padx=10, pady=10)

    Label(tab_accounts, text="Name").grid(row=3, column=0, padx=10, pady=5)
    entry_account_name = Entry(tab_accounts)
    entry_account_name.grid(row=3, column=1, padx=10, pady=5)
    Label(tab_accounts, text="Balance").grid(row=4, column=0, padx=10, pady=5)
    entry_account_balance = Entry(tab_accounts)
    entry_account_balance.grid(row=4, column=1, padx=10, pady=5)
    Button(tab_accounts, text="Add Account", command=lambda: add_account(entry_account_name.get(), float(entry_account_balance.get()))).grid(row=5, column=0, columnspan=2, pady=10)

    # Inventory Tab

    # Inventory Tab
    Label(tab_inventory, text="Inventory Management").grid(row=0, column=0, padx=10, pady=10)

    inventory_tree = ttk.Treeview(tab_inventory, columns=("ID", "Item Name", "Quantity", "Price"), show='headings')
    inventory_tree.heading("ID", text="ID")
    inventory_tree.heading("Item Name", text="Item Name")
    inventory_tree.heading("Quantity", text="Quantity")
    inventory_tree.heading("Price", text="Price")
    inventory_tree.grid(row=1, column=0, padx=10, pady=10)

    Button(tab_inventory, text="View Inventory", command=lambda: populate_treeview(inventory_tree, view_inventory())).grid(row=2, column=0, padx=10, pady=10)

    Label(tab_inventory, text="Item Name").grid(row=3, column=0, padx=10, pady=5)
    entry_item_name = Entry(tab_inventory)
    entry_item_name.grid(row=3, column=1, padx=10, pady=5)
    Label(tab_inventory, text="Quantity").grid(row=4, column=0, padx=10, pady=5)
    entry_quantity = Entry(tab_inventory)
    entry_quantity.grid(row=4, column=1, padx=10, pady=5)
    Label(tab_inventory, text="Price").grid(row=5, column=0, padx=10, pady=5)
    entry_price = Entry(tab_inventory)
    entry_price.grid(row=5, column=1, padx=10, pady=5)
    Button(tab_inventory, text="Add Item", command=lambda: add_inventory_item(entry_item_name.get(), int(entry_quantity.get()), float(entry_price.get()))).grid,Button(tab_inventory, text="Add Item", command=lambda: add_inventory_item(entry_item_name.get(), int(entry_quantity.get()), float(entry_price.get()))).grid(row=6, column=0, columnspan=2, pady=10)

    # Sales Tab
    Label(tab_sales, text="Sales Management").grid(row=0, column=0, padx=10, pady=10)

    sales_tree = ttk.Treeview(tab_sales, columns=("ID", "Item ID", "Quantity", "Date"), show='headings')
    sales_tree.heading("ID", text="ID")
    sales_tree.heading("Item ID", text="Item ID")
    sales_tree.heading("Quantity", text="Quantity")
    sales_tree.heading("Date", text="Date")
    sales_tree.grid(row=1, column=0, padx=10, pady=10)

    Button(tab_sales, text="View Sales", command=lambda: populate_treeview(sales_tree, view_sales())).grid(row=2, column=0, padx=10, pady=10)
    Button(tab_sales, text="Record Sale", command=lambda: record_sale(1, 5, "2024-11-19")).grid(row=3, column=0, columnspan=2, pady=10)

    main_app.mainloop()
    print("Main application loop is running...")

# Function to populate the Treeview widget
def populate_treeview(treeview, data):
    for row in treeview.get_children():
        treeview.delete(row)
    for row in data:
        treeview.insert("", "end", values=row)
    print(f"Populated Treeview with data: {data}")

# Function to open the registration window
def open_registration_window():
    reg_window = Toplevel(root)
    reg_window.title("Register")
    print("Registration window opened.")

    Label(reg_window, text="Username").grid(row=0, column=0, padx=10, pady=5)
    reg_username = Entry(reg_window)
    reg_username.grid(row=0, column=1, padx=10, pady=5)

    Label(reg_window, text="Password").grid(row=1, column=0, padx=10, pady=5)
    reg_password = Entry(reg_window, show='*')
    reg_password.grid(row=1, column=1, padx=10, pady=5)

    Label(reg_window, text="Role").grid(row=2, column=0, padx=10, pady=5)
    reg_role = Entry(reg_window)
    reg_role.grid(row=2, column=1, padx=10, pady=5)

    Button(reg_window, text="Register", command=lambda: register_user(reg_username.get(), reg_password.get(), reg_role.get())).grid(row=3, column=0, columnspan=2, pady=10)

# Create the main application window
root = Tk()
root.title("TK MNGMNT")
print("Login window created.")

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    user = login_user(username, password)
    if user:
        messagebox.showinfo("Login Success", f"Welcome {username}!")
        root.destroy()  # Close login window and open main application
        open_main_application()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Login screen
login_frame = Frame(root)
login_frame.pack(pady=20)

label_username = Label(login_frame, text="Username")
label_username.grid(row=0, column=0, padx=10, pady=5)
entry_username = Entry(login_frame)
entry_username.grid(row=0, column=1, padx=10, pady=5)

label_password = Label(login_frame, text="Password")
label_password.grid(row=1, column=0, padx=10, pady=5)
entry_password = Entry(login_frame, show='*')
entry_password.grid(row=1, column=1, padx=10, pady=5)

button_login = Button(login_frame, text="Login", command=login)
button_login.grid(row=2, column=0, columnspan=2, pady=10)

button_register = Button(login_frame, text="Register", command=open_registration_window)
button_register.grid(row=3, column=0, columnspan=2, pady=10)

# Run the GUI main loop
root.mainloop()
print("GUI main loop is running...")
