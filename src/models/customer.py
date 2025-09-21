"""
Customer Model for Business Management App
"""

from datetime import datetime
from controllers.database_controller import DatabaseController

class Customer:
    """Customer model class"""
    
    def __init__(self, id=None, name=None, phone=None, email=None, address=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.created_at = None
        self.updated_at = None
        self.db = DatabaseController()
    
    def save(self):
        """Save customer to database"""
        try:
            if self.id is None:
                # Insert new customer
                query = '''
                    INSERT INTO customers (name, phone, email, address)
                    VALUES (?, ?, ?, ?)
                '''
                params = (self.name, self.phone, self.email, self.address)
                self.id = self.db.execute_query(query, params)
            else:
                # Update existing customer
                query = '''
                    UPDATE customers 
                    SET name = ?, phone = ?, email = ?, address = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                '''
                params = (self.name, self.phone, self.email, self.address, self.id)
                self.db.execute_query(query, params)
            
            return True
        except Exception as e:
            print(f"Error saving customer: {e}")
            return False
    
    def delete(self):
        """Delete customer from database"""
        try:
            if self.id is None:
                return False
            
            query = "DELETE FROM customers WHERE id = ?"
            self.db.execute_query(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting customer: {e}")
            return False
    
    @classmethod
    def get_by_id(cls, customer_id):
        """Get customer by ID"""
        try:
            db = DatabaseController()
            query = "SELECT * FROM customers WHERE id = ?"
            result = db.execute_query(query, (customer_id,))
            
            if result:
                data = result[0]
                customer = cls(
                    id=data['id'],
                    name=data['name'],
                    phone=data['phone'],
                    email=data['email'],
                    address=data['address']
                )
                customer.created_at = data['created_at']
                customer.updated_at = data['updated_at']
                return customer
            return None
        except Exception as e:
            print(f"Error getting customer: {e}")
            return None
    
    @classmethod
    def get_all(cls):
        """Get all customers"""
        try:
            db = DatabaseController()
            query = "SELECT * FROM customers ORDER BY name"
            results = db.execute_query(query)
            
            customers = []
            for data in results:
                customer = cls(
                    id=data['id'],
                    name=data['name'],
                    phone=data['phone'],
                    email=data['email'],
                    address=data['address']
                )
                customer.created_at = data['created_at']
                customer.updated_at = data['updated_at']
                customers.append(customer)
            
            return customers
        except Exception as e:
            print(f"Error getting customers: {e}")
            return []
    
    @classmethod
    def search(cls, keyword):
        """Search customers by name, phone, or email"""
        try:
            db = DatabaseController()
            query = '''
                SELECT * FROM customers 
                WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
                ORDER BY name
            '''
            search_term = f"%{keyword}%"
            results = db.execute_query(query, (search_term, search_term, search_term))
            
            customers = []
            for data in results:
                customer = cls(
                    id=data['id'],
                    name=data['name'],
                    phone=data['phone'],
                    email=data['email'],
                    address=data['address']
                )
                customer.created_at = data['created_at']
                customer.updated_at = data['updated_at']
                customers.append(customer)
            
            return customers
        except Exception as e:
            print(f"Error searching customers: {e}")
            return []
    
    def to_dict(self):
        """Convert customer to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __str__(self):
        return f"Customer(id={self.id}, name='{self.name}', phone='{self.phone}')"