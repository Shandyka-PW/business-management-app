"""
Database Controller for Business Management App
Handles all database operations and schema management
"""

import sqlite3
import os
import json
from datetime import datetime
from utils.config import Config

class DatabaseController:
    """Controller for database operations"""
    
    def __init__(self):
        self.config = Config()
        self.db_path = self.config.get_database_path()
        self.connection = None
    
    def get_connection(self):
        """Get database connection"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self):
        """Initialize database with all tables"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create tables
            self.create_tables(cursor)
            
            # Insert default data
            self.insert_default_data(cursor)
            
            conn.commit()
            print("Database initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False
    
    def create_tables(self, cursor):
        """Create all database tables"""
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                cost REAL,
                stock INTEGER DEFAULT 0,
                unit TEXT DEFAULT 'pcs',
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number TEXT UNIQUE NOT NULL,
                customer_id INTEGER,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                status TEXT DEFAULT 'pending',
                total_amount REAL NOT NULL,
                paid_amount REAL DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # Order items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Processes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                assigned_to TEXT,
                start_date TIMESTAMP,
                due_date TIMESTAMP,
                completed_date TIMESTAMP,
                order_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (id)
            )
        ''')
        
        # Financial transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reference_id TEXT,
                reference_type TEXT,
                payment_method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (reference_id) REFERENCES orders (id)
            )
        ''')
        
        # Invoices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                order_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                status TEXT DEFAULT 'unpaid',
                subtotal REAL NOT NULL,
                tax_rate REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                total_amount REAL NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_processes_order ON processes(order_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_financial_date ON financial_transactions(date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_invoices_order ON invoices(order_id)')
        
    def insert_default_data(self, cursor):
        """Insert default data into tables"""
        
        # Insert default categories
        categories = [
            ('product_category', 'Elektronik', 'Kategori produk elektronik'),
            ('product_category', 'Fashion', 'Kategori produk fashion'),
            ('product_category', 'Makanan', 'Kategori produk makanan'),
            ('product_category', 'Jasa', 'Kategori produk jasa'),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO settings (key, value, description) 
            VALUES (?, ?, ?)
        ''', categories)
        
        # Insert default settings
        settings = [
            ('company_name', 'Your Company Name', 'Nama perusahaan'),
            ('company_address', 'Company Address', 'Alamat perusahaan'),
            ('company_phone', '+62 123 456 789', 'Nomor telepon perusahaan'),
            ('company_email', 'company@email.com', 'Email perusahaan'),
            ('currency', 'IDR', 'Mata uang'),
            ('tax_rate', '10', 'Persentase pajak'),
            ('invoice_prefix', 'INV', 'Prefix nomor invoice'),
            ('order_prefix', 'ORD', 'Prefix nomor order'),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO settings (key, value, description) 
            VALUES (?, ?, ?)
        ''', settings)
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                conn.commit()
                return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
                
        except Exception as e:
            print(f"Database error: {e}")
            conn.rollback()
            raise
    
    def execute_many(self, query, params_list):
        """Execute query multiple times with different parameters"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Database error: {e}")
            conn.rollback()
            raise
    
    def get_setting(self, key, default=None):
        """Get setting value"""
        try:
            result = self.execute_query(
                "SELECT value FROM settings WHERE key = ?", 
                (key,)
            )
            return result[0]['value'] if result else default
        except:
            return default
    
    def set_setting(self, key, value, description=None):
        """Set setting value"""
        try:
            if description:
                self.execute_query('''
                    INSERT OR REPLACE INTO settings (key, value, description) 
                    VALUES (?, ?, ?)
                ''', (key, value, description))
            else:
                self.execute_query('''
                    INSERT OR REPLACE INTO settings (key, value) 
                    VALUES (?, ?)
                ''', (key, value))
            return True
        except Exception as e:
            print(f"Error setting value: {e}")
            return False
    
    def generate_number(self, prefix, table, field):
        """Generate unique number with prefix"""
        try:
            # Get current date
            date_str = datetime.now().strftime("%Y%m%d")
            
            # Get last number
            result = self.execute_query(f'''
                SELECT {field} FROM {table} 
                WHERE {field} LIKE ? 
                ORDER BY {field} DESC 
                LIMIT 1
            ''', (f"{prefix}{date_str}%",))
            
            if result:
                last_number = result[0][field]
                # Extract sequence number
                try:
                    sequence = int(last_number[-4:]) + 1
                except:
                    sequence = 1
            else:
                sequence = 1
            
            # Format new number
            new_number = f"{prefix}{date_str}{sequence:04d}"
            return new_number
            
        except Exception as e:
            print(f"Error generating number: {e}")
            return f"{prefix}{datetime.now().strftime('%Y%m%d')}0001"
    
    def backup_database(self, backup_path=None):
        """Backup database to specified path"""
        try:
            if backup_path is None:
                backup_path = self.config.get_backup_path()
            
            # Create backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_path, f"business_backup_{timestamp}.db")
            
            # Close current connection
            self.close_connection()
            
            # Copy database file
            import shutil
            shutil.copy2(self.db_path, backup_file)
            
            # Reopen connection
            self.get_connection()
            
            print(f"Database backed up to: {backup_file}")
            return backup_file
            
        except Exception as e:
            print(f"Error backing up database: {e}")
            return None
    
    def restore_database(self, backup_file):
        """Restore database from backup file"""
        try:
            if not os.path.exists(backup_file):
                raise FileNotFoundError(f"Backup file not found: {backup_file}")
            
            # Close current connection
            self.close_connection()
            
            # Copy backup file to database location
            import shutil
            shutil.copy2(backup_file, self.db_path)
            
            # Reopen connection
            self.get_connection()
            
            print(f"Database restored from: {backup_file}")
            return True
            
        except Exception as e:
            print(f"Error restoring database: {e}")
            return False
    
    def get_database_info(self):
        """Get database information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get table info
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Get record counts
            info = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                info[table] = count
            
            # Get database size
            db_size = os.path.getsize(self.db_path)
            
            return {
                "tables": info,
                "database_size": db_size,
                "database_path": self.db_path
            }
            
        except Exception as e:
            print(f"Error getting database info: {e}")
            return {}