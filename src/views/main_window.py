"""
Main Window for Business Management App
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.database_controller import DatabaseController
from controllers.license_controller import LicenseController
from models.customer import Customer
from models.product import Product
from models.order import Order
from utils.config import Config

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Business Management App")
        self.root.geometry("1200x800")
        
        # Initialize controllers
        self.db = DatabaseController()
        self.license_controller = LicenseController()
        self.config = Config()
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("resources/icon.ico")
        except:
            pass
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.configure_styles()
        
        # Create main layout
        self.create_main_layout()
        
        # Create menu
        self.create_menu()
        
        # Load dashboard data
        self.load_dashboard_data()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def configure_styles(self):
        """Configure custom styles"""
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Card.TFrame', relief='raised', borderwidth=1)
        self.style.configure('Nav.TButton', font=('Arial', 10))
        self.style.configure('Success.TLabel', foreground='green')
        self.style.configure('Warning.TLabel', foreground='orange')
        self.style.configure('Danger.TLabel', foreground='red')
    
    def create_main_layout(self):
        """Create main application layout"""
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create header
        self.create_header(main_container)
        
        # Create content area
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create navigation sidebar
        self.create_navigation(content_frame)
        
        # Create main content area
        self.create_main_content(content_frame)
        
        # Create status bar
        self.create_status_bar()
    
    def create_header(self, parent):
        """Create application header"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # App title
        title_label = ttk.Label(header_frame, text="Business Management App", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # User info
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(side=tk.RIGHT)
        
        company_name = self.config.get('company_name', 'Your Company')
        user_label = ttk.Label(user_frame, text=f"Company: {company_name}")
        user_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Date/time
        self.datetime_label = ttk.Label(user_frame, text="")
        self.datetime_label.pack(side=tk.LEFT)
        
        # Update datetime
        self.update_datetime()
    
    def create_navigation(self, parent):
        """Create navigation sidebar"""
        nav_frame = ttk.Frame(parent, width=200)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        nav_frame.pack_propagate(False)
        
        # Navigation title
        nav_title = ttk.Label(nav_frame, text="Navigation", style='Header.TLabel')
        nav_title.pack(pady=(0, 10))
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Customers", self.show_customers),
            ("Products", self.show_products),
            ("Orders", self.show_orders),
            ("Processes", self.show_processes),
            ("Finance", self.show_finance),
            ("Invoices", self.show_invoices),
            ("Reports", self.show_reports)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(nav_frame, text=text, style='Nav.TButton',
                           command=command, width=25)
            btn.pack(pady=2)
        
        # Settings section
        ttk.Separator(nav_frame, orient='horizontal').pack(fill=tk.X, pady=20)
        
        settings_label = ttk.Label(nav_frame, text="Settings", style='Header.TLabel')
        settings_label.pack(pady=(0, 10))
        
        settings_buttons = [
            ("Backup Database", self.backup_database),
            ("Restore Database", self.restore_database),
            ("Settings", self.show_settings),
            ("About", self.show_about)
        ]
        
        for text, command in settings_buttons:
            btn = ttk.Button(nav_frame, text=text, style='Nav.TButton',
                           command=command, width=25)
            btn.pack(pady=2)
    
    def create_main_content(self, parent):
        """Create main content area"""
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_customers_tab()
        self.create_products_tab()
        self.create_orders_tab()
        self.create_processes_tab()
        self.create_finance_tab()
        self.create_invoices_tab()
        self.create_reports_tab()
    
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        
        # Create dashboard content
        self.create_dashboard_content()
    
    def create_dashboard_content(self):
        """Create dashboard content"""
        # Main container
        container = ttk.Frame(self.dashboard_frame, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(container, text="Dashboard Overview", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Stats cards frame
        stats_frame = ttk.Frame(container)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create stats cards
        self.stats_cards = {}
        
        # Customers card
        customers_card = self.create_stats_card(stats_frame, "Total Customers", "0", "blue")
        customers_card.grid(row=0, column=0, padx=5, sticky="ew")
        self.stats_cards['customers'] = customers_card
        
        # Products card
        products_card = self.create_stats_card(stats_frame, "Total Products", "0", "green")
        products_card.grid(row=0, column=1, padx=5, sticky="ew")
        self.stats_cards['products'] = products_card
        
        # Orders card
        orders_card = self.create_stats_card(stats_frame, "Total Orders", "0", "orange")
        orders_card.grid(row=0, column=2, padx=5, sticky="ew")
        self.stats_cards['orders'] = orders_card
        
        # Revenue card
        revenue_card = self.create_stats_card(stats_frame, "Total Revenue", "Rp 0", "purple")
        revenue_card.grid(row=0, column=3, padx=5, sticky="ew")
        self.stats_cards['revenue'] = revenue_card
        
        # Configure grid weights
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)
        
        # Recent activities frame
        activities_frame = ttk.LabelFrame(container, text="Recent Activities", padding="10")
        activities_frame.pack(fill=tk.BOTH, expand=True)
        
        # Activities treeview
        self.activities_tree = ttk.Treeview(activities_frame, columns=('date', 'type', 'description'), 
                                          show='headings', height=10)
        
        self.activities_tree.heading('date', text='Date')
        self.activities_tree.heading('type', text='Type')
        self.activities_tree.heading('description', text='Description')
        
        self.activities_tree.column('date', width=150)
        self.activities_tree.column('type', width=100)
        self.activities_tree.column('description', width=400)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(activities_frame, orient=tk.VERTICAL, 
                                 command=self.activities_tree.yview)
        self.activities_tree.configure(yscrollcommand=scrollbar.set)
        
        self.activities_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_stats_card(self, parent, title, value, color):
        """Create a statistics card"""
        card_frame = ttk.Frame(parent, style='Card.TFrame')
        
        # Title
        title_label = ttk.Label(card_frame, text=title, font=('Arial', 10, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Value
        value_label = ttk.Label(card_frame, text=value, font=('Arial', 18, 'bold'))
        value_label.pack(pady=(0, 10))
        
        return card_frame
    
    def create_customers_tab(self):
        """Create customers tab"""
        self.customers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.customers_frame, text="Customers")
        
        # Create customers content
        self.create_customers_content()
    
    def create_customers_content(self):
        """Create customers management content"""
        # Main container
        container = ttk.Frame(self.customers_frame, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Title and buttons
        header_frame = ttk.Frame(container)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Customer Management", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Buttons
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="Add Customer", 
                  command=self.add_customer).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Edit Customer", 
                  command=self.edit_customer).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete Customer", 
                  command=self.delete_customer).pack(side=tk.LEFT, padx=2)
        
        # Search frame
        search_frame = ttk.Frame(container)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.customer_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.customer_search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        search_entry.bind('<KeyRelease>', lambda e: self.search_customers())
        
        ttk.Button(search_frame, text="Search", 
                  command=self.search_customers).pack(side=tk.LEFT)
        
        # Customers treeview
        self.customers_tree = ttk.Treeview(container, 
                                         columns=('id', 'name', 'phone', 'email', 'address'), 
                                         show='headings')
        
        self.customers_tree.heading('id', text='ID')
        self.customers_tree.heading('name', text='Name')
        self.customers_tree.heading('phone', text='Phone')
        self.customers_tree.heading('email', text='Email')
        self.customers_tree.heading('address', text='Address')
        
        self.customers_tree.column('id', width=50)
        self.customers_tree.column('name', width=200)
        self.customers_tree.column('phone', width=150)
        self.customers_tree.column('email', width=200)
        self.customers_tree.column('address', width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, 
                                 command=self.customers_tree.yview)
        self.customers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.customers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load customers
        self.load_customers()
    
    def create_products_tab(self):
        """Create products tab"""
        self.products_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.products_frame, text="Products")
        
        # Create products content
        self.create_products_content()
    
    def create_products_content(self):
        """Create products management content"""
        # Main container
        container = ttk.Frame(self.products_frame, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Title and buttons
        header_frame = ttk.Frame(container)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Product Management", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Buttons
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="Add Product", 
                  command=self.add_product).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Edit Product", 
                  command=self.edit_product).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete Product", 
                  command=self.delete_product).pack(side=tk.LEFT, padx=2)
        
        # Search frame
        search_frame = ttk.Frame(container)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.product_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.product_search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        search_entry.bind('<KeyRelease>', lambda e: self.search_products())
        
        ttk.Button(search_frame, text="Search", 
                  command=self.search_products).pack(side=tk.LEFT)
        
        # Products treeview
        self.products_tree = ttk.Treeview(container, 
                                        columns=('id', 'name', 'price', 'stock', 'category'), 
                                        show='headings')
        
        self.products_tree.heading('id', text='ID')
        self.products_tree.heading('name', text='Name')
        self.products_tree.heading('price', text='Price')
        self.products_tree.heading('stock', text='Stock')
        self.products_tree.heading('category', text='Category')
        
        self.products_tree.column('id', width=50)
        self.products_tree.column('name', width=200)
        self.products_tree.column('price', width=100)
        self.products_tree.column('stock', width=80)
        self.products_tree.column('category', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, 
                                 command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load products
        self.load_products()
    
    def create_orders_tab(self):
        """Create orders tab"""
        self.orders_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.orders_frame, text="Orders")
        
        # Create orders content
        self.create_orders_content()
    
    def create_orders_content(self):
        """Create orders management content"""
        # Main container
        container = ttk.Frame(self.orders_frame, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Title and buttons
        header_frame = ttk.Frame(container)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Order Management", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Buttons
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="New Order", 
                  command=self.new_order).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Edit Order", 
                  command=self.edit_order).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete Order", 
                  command=self.delete_order).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Add Payment", 
                  command=self.add_payment).pack(side=tk.LEFT, padx=2)
        
        # Filter frame
        filter_frame = ttk.Frame(container)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.order_filter_var = tk.StringVar(value="all")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.order_filter_var, 
                                   values=["all", "pending", "paid", "unpaid"], 
                                   state="readonly", width=15)
        filter_combo.pack(side=tk.LEFT, padx=(0, 5))
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_orders())
        
        # Orders treeview
        self.orders_tree = ttk.Treeview(container, 
                                       columns=('id', 'order_number', 'customer', 'status', 
                                              'total_amount', 'paid_amount', 'order_date'), 
                                       show='headings')
        
        self.orders_tree.heading('id', text='ID')
        self.orders_tree.heading('order_number', text='Order #')
        self.orders_tree.heading('customer', text='Customer')
        self.orders_tree.heading('status', text='Status')
        self.orders_tree.heading('total_amount', text='Total')
        self.orders_tree.heading('paid_amount', text='Paid')
        self.orders_tree.heading('order_date', text='Date')
        
        self.orders_tree.column('id', width=50)
        self.orders_tree.column('order_number', width=120)
        self.orders_tree.column('customer', width=150)
        self.orders_tree.column('status', width=100)
        self.orders_tree.column('total_amount', width=100)
        self.orders_tree.column('paid_amount', width=100)
        self.orders_tree.column('order_date', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, 
                                 command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load orders
        self.load_orders()
    
    def create_processes_tab(self):
        """Create processes tab"""
        self.processes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.processes_frame, text="Processes")
        
        # Placeholder content
        placeholder = ttk.Label(self.processes_frame, text="Process Management - Coming Soon", 
                               font=('Arial', 16))
        placeholder.pack(expand=True)
    
    def create_finance_tab(self):
        """Create finance tab"""
        self.finance_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.finance_frame, text="Finance")
        
        # Placeholder content
        placeholder = ttk.Label(self.finance_frame, text="Finance Management - Coming Soon", 
                               font=('Arial', 16))
        placeholder.pack(expand=True)
    
    def create_invoices_tab(self):
        """Create invoices tab"""
        self.invoices_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.invoices_frame, text="Invoices")
        
        # Placeholder content
        placeholder = ttk.Label(self.invoices_frame, text="Invoice Management - Coming Soon", 
                               font=('Arial', 16))
        placeholder.pack(expand=True)
    
    def create_reports_tab(self):
        """Create reports tab"""
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text="Reports")
        
        # Placeholder content
        placeholder = ttk.Label(self.reports_frame, text="Reports - Coming Soon", 
                               font=('Arial', 16))
        placeholder.pack(expand=True)
    
    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Backup Database", command=self.backup_database)
        file_menu.add_command(label="Restore Database", command=self.restore_database)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Settings", command=self.show_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="License Info", command=self.show_license_info)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready", relief=tk.SUNKEN)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # License info
        license_info = self.license_controller.get_license_info()
        if license_info:
            license_text = f"Licensed: {license_info.get('license_key', 'Unknown')}"
        else:
            license_text = "Unlicensed"
        
        self.license_label = ttk.Label(self.status_bar, text=license_text, relief=tk.SUNKEN)
        self.license_label.pack(side=tk.RIGHT)
    
    def update_datetime(self):
        """Update date/time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.datetime_label.config(text=current_time)
        self.root.after(1000, self.update_datetime)  # Update every second
    
    def load_dashboard_data(self):
        """Load dashboard data"""
        try:
            # Get statistics
            customers_count = len(Customer.get_all())
            products_count = len(Product.get_all())
            orders_count = len(Order.get_all())
            
            # Calculate total revenue
            total_revenue = 0
            orders = Order.get_all()
            for order in orders:
                total_revenue += order.paid_amount
            
            # Update stats cards
            self.stats_cards['customers'].children['!label2'].config(text=str(customers_count))
            self.stats_cards['products'].children['!label2'].config(text=str(products_count))
            self.stats_cards['orders'].children['!label2'].config(text=str(orders_count))
            self.stats_cards['revenue'].children['!label2'].config(text=f"Rp {total_revenue:,.0f}")
            
            # Load recent activities (placeholder)
            self.activities_tree.delete(*self.activities_tree.get_children())
            activities = [
                (datetime.now().strftime("%Y-%m-%d %H:%M"), "System", "Application started"),
                (datetime.now().strftime("%Y-%m-%d %H:%M"), "Dashboard", "Data loaded"),
            ]
            
            for activity in activities:
                self.activities_tree.insert('', 'end', values=activity)
            
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
    
    def load_customers(self):
        """Load customers data"""
        try:
            customers = Customer.get_all()
            self.customers_tree.delete(*self.customers_tree.get_children())
            
            for customer in customers:
                self.customers_tree.insert('', 'end', values=(
                    customer.id, customer.name, customer.phone, customer.email, customer.address
                ))
                
        except Exception as e:
            print(f"Error loading customers: {e}")
    
    def load_products(self):
        """Load products data"""
        try:
            products = Product.get_all()
            self.products_tree.delete(*self.products_tree.get_children())
            
            for product in products:
                self.products_tree.insert('', 'end', values=(
                    product.id, product.name, f"Rp {product.price:,.0f}", 
                    product.stock, product.category
                ))
                
        except Exception as e:
            print(f"Error loading products: {e}")
    
    def load_orders(self):
        """Load orders data"""
        try:
            orders = Order.get_all()
            self.orders_tree.delete(*self.orders_tree.get_children())
            
            for order in orders:
                customer = order.get_customer()
                customer_name = customer.name if customer else "Unknown"
                
                self.orders_tree.insert('', 'end', values=(
                    order.id, order.order_number, customer_name, order.status,
                    f"Rp {order.total_amount:,.0f}", f"Rp {order.paid_amount:,.0f}",
                    order.order_date
                ))
                
        except Exception as e:
            print(f"Error loading orders: {e}")
    
    def show_dashboard(self):
        """Show dashboard tab"""
        self.notebook.select(0)
    
    def show_customers(self):
        """Show customers tab"""
        self.notebook.select(1)
    
    def show_products(self):
        """Show products tab"""
        self.notebook.select(2)
    
    def show_orders(self):
        """Show orders tab"""
        self.notebook.select(3)
    
    def show_processes(self):
        """Show processes tab"""
        self.notebook.select(4)
    
    def show_finance(self):
        """Show finance tab"""
        self.notebook.select(5)
    
    def show_invoices(self):
        """Show invoices tab"""
        self.notebook.select(6)
    
    def show_reports(self):
        """Show reports tab"""
        self.notebook.select(7)
    
    def search_customers(self):
        """Search customers"""
        keyword = self.customer_search_var.get().strip()
        if keyword:
            customers = Customer.search(keyword)
        else:
            customers = Customer.get_all()
        
        self.customers_tree.delete(*self.customers_tree.get_children())
        for customer in customers:
            self.customers_tree.insert('', 'end', values=(
                customer.id, customer.name, customer.phone, customer.email, customer.address
            ))
    
    def search_products(self):
        """Search products"""
        keyword = self.product_search_var.get().strip()
        if keyword:
            products = Product.search(keyword)
        else:
            products = Product.get_all()
        
        self.products_tree.delete(*self.products_tree.get_children())
        for product in products:
            self.products_tree.insert('', 'end', values=(
                product.id, product.name, f"Rp {product.price:,.0f}", 
                product.stock, product.category
            ))
    
    def filter_orders(self):
        """Filter orders by status"""
        filter_value = self.order_filter_var.get()
        
        if filter_value == "all":
            orders = Order.get_all()
        elif filter_value == "unpaid":
            orders = Order.get_unpaid()
        else:
            orders = Order.get_by_status(filter_value)
        
        self.orders_tree.delete(*self.orders_tree.get_children())
        for order in orders:
            customer = order.get_customer()
            customer_name = customer.name if customer else "Unknown"
            
            self.orders_tree.insert('', 'end', values=(
                order.id, order.order_number, customer_name, order.status,
                f"Rp {order.total_amount:,.0f}", f"Rp {order.paid_amount:,.0f}",
                order.order_date
            ))
    
    def add_customer(self):
        """Add new customer"""
        messagebox.showinfo("Info", "Add Customer feature - Coming Soon")
    
    def edit_customer(self):
        """Edit customer"""
        messagebox.showinfo("Info", "Edit Customer feature - Coming Soon")
    
    def delete_customer(self):
        """Delete customer"""
        messagebox.showinfo("Info", "Delete Customer feature - Coming Soon")
    
    def add_product(self):
        """Add new product"""
        messagebox.showinfo("Info", "Add Product feature - Coming Soon")
    
    def edit_product(self):
        """Edit product"""
        messagebox.showinfo("Info", "Edit Product feature - Coming Soon")
    
    def delete_product(self):
        """Delete product"""
        messagebox.showinfo("Info", "Delete Product feature - Coming Soon")
    
    def new_order(self):
        """Create new order"""
        messagebox.showinfo("Info", "New Order feature - Coming Soon")
    
    def edit_order(self):
        """Edit order"""
        messagebox.showinfo("Info", "Edit Order feature - Coming Soon")
    
    def delete_order(self):
        """Delete order"""
        messagebox.showinfo("Info", "Delete Order feature - Coming Soon")
    
    def add_payment(self):
        """Add payment to order"""
        messagebox.showinfo("Info", "Add Payment feature - Coming Soon")
    
    def backup_database(self):
        """Backup database"""
        try:
            backup_path = filedialog.asksaveasfilename(
                title="Backup Database",
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            
            if backup_path:
                result = self.db.backup_database(backup_path)
                if result:
                    messagebox.showinfo("Success", f"Database backed up to:\n{result}")
                else:
                    messagebox.showerror("Error", "Failed to backup database")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
    
    def restore_database(self):
        """Restore database from backup"""
        try:
            backup_path = filedialog.askopenfilename(
                title="Restore Database",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            
            if backup_path:
                if messagebox.askyesno("Confirm", 
                                      "Are you sure you want to restore database?\nThis will replace all current data!"):
                    result = self.db.restore_database(backup_path)
                    if result:
                        messagebox.showinfo("Success", "Database restored successfully")
                        # Reload all data
                        self.load_dashboard_data()
                        self.load_customers()
                        self.load_products()
                        self.load_orders()
                    else:
                        messagebox.showerror("Error", "Failed to restore database")
        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {str(e)}")
    
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo("Info", "Settings feature - Coming Soon")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Business Management App v1.0.0

A comprehensive business management application for:
- Customer management
- Product management  
- Order processing
- Financial tracking
- Invoice generation

Developed with Python and Tkinter
Offline capable with SQLite database

© 2024 Business Management App"""
        
        messagebox.showinfo("About", about_text)
    
    def show_license_info(self):
        """Show license information"""
        license_info = self.license_controller.get_license_info()
        
        if license_info:
            info_text = f"""License Information

License Key: {license_info.get('license_key', 'Unknown')}
Hardware ID: {license_info.get('current_hardware_id', 'Unknown')}
Status: {'Valid' if license_info.get('is_valid', False) else 'Invalid'}

Saved Date: {license_info.get('saved_date', 'Unknown')}"""
        else:
            info_text = """No license information found.

Please contact your administrator to obtain a valid license key."""
        
        messagebox.showinfo("License Info", info_text)
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            # Close database connection
            self.db.close_connection()
            self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()