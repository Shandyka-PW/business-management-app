"""
Product Model for Business Management App
"""

from datetime import datetime
from controllers.database_controller import DatabaseController

class Product:
    """Product model class"""
    
    def __init__(self, id=None, name=None, description=None, price=None, cost=None, 
                 stock=0, unit='pcs', category=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.cost = cost
        self.stock = stock
        self.unit = unit
        self.category = category
        self.created_at = None
        self.updated_at = None
        self.db = DatabaseController()
    
    def save(self):
        """Save product to database"""
        try:
            if self.id is None:
                # Insert new product
                query = '''
                    INSERT INTO products (name, description, price, cost, stock, unit, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                '''
                params = (self.name, self.description, self.price, self.cost, 
                         self.stock, self.unit, self.category)
                self.id = self.db.execute_query(query, params)
            else:
                # Update existing product
                query = '''
                    UPDATE products 
                    SET name = ?, description = ?, price = ?, cost = ?, stock = ?, 
                        unit = ?, category = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                '''
                params = (self.name, self.description, self.price, self.cost, 
                         self.stock, self.unit, self.category, self.id)
                self.db.execute_query(query, params)
            
            return True
        except Exception as e:
            print(f"Error saving product: {e}")
            return False
    
    def delete(self):
        """Delete product from database"""
        try:
            if self.id is None:
                return False
            
            query = "DELETE FROM products WHERE id = ?"
            self.db.execute_query(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    
    def update_stock(self, quantity):
        """Update product stock"""
        try:
            if self.id is None:
                return False
            
            new_stock = self.stock + quantity
            query = "UPDATE products SET stock = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            self.db.execute_query(query, (new_stock, self.id))
            self.stock = new_stock
            return True
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False
    
    @classmethod
    def get_by_id(cls, product_id):
        """Get product by ID"""
        try:
            db = DatabaseController()
            query = "SELECT * FROM products WHERE id = ?"
            result = db.execute_query(query, (product_id,))
            
            if result:
                data = result[0]
                product = cls(
                    id=data['id'],
                    name=data['name'],
                    description=data['description'],
                    price=data['price'],
                    cost=data['cost'],
                    stock=data['stock'],
                    unit=data['unit'],
                    category=data['category']
                )
                product.created_at = data['created_at']
                product.updated_at = data['updated_at']
                return product
            return None
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
    
    @classmethod
    def get_all(cls):
        """Get all products"""
        try:
            db = DatabaseController()
            query = "SELECT * FROM products ORDER BY name"
            results = db.execute_query(query)
            
            products = []
            for data in results:
                product = cls(
                    id=data['id'],
                    name=data['name'],
                    description=data['description'],
                    price=data['price'],
                    cost=data['cost'],
                    stock=data['stock'],
                    unit=data['unit'],
                    category=data['category']
                )
                product.created_at = data['created_at']
                product.updated_at = data['updated_at']
                products.append(product)
            
            return products
        except Exception as e:
            print(f"Error getting products: {e}")
            return []
    
    @classmethod
    def get_low_stock(cls, threshold=10):
        """Get products with low stock"""
        try:
            db = DatabaseController()
            query = "SELECT * FROM products WHERE stock <= ? ORDER BY stock"
            results = db.execute_query(query, (threshold,))
            
            products = []
            for data in results:
                product = cls(
                    id=data['id'],
                    name=data['name'],
                    description=data['description'],
                    price=data['price'],
                    cost=data['cost'],
                    stock=data['stock'],
                    unit=data['unit'],
                    category=data['category']
                )
                product.created_at = data['created_at']
                product.updated_at = data['updated_at']
                products.append(product)
            
            return products
        except Exception as e:
            print(f"Error getting low stock products: {e}")
            return []
    
    @classmethod
    def search(cls, keyword):
        """Search products by name or category"""
        try:
            db = DatabaseController()
            query = '''
                SELECT * FROM products 
                WHERE name LIKE ? OR category LIKE ?
                ORDER BY name
            '''
            search_term = f"%{keyword}%"
            results = db.execute_query(query, (search_term, search_term))
            
            products = []
            for data in results:
                product = cls(
                    id=data['id'],
                    name=data['name'],
                    description=data['description'],
                    price=data['price'],
                    cost=data['cost'],
                    stock=data['stock'],
                    unit=data['unit'],
                    category=data['category']
                )
                product.created_at = data['created_at']
                product.updated_at = data['updated_at']
                products.append(product)
            
            return products
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    @classmethod
    def get_categories(cls):
        """Get all product categories"""
        try:
            db = DatabaseController()
            query = "SELECT DISTINCT category FROM products WHERE category IS NOT NULL ORDER BY category"
            results = db.execute_query(query)
            return [row['category'] for row in results]
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'cost': self.cost,
            'stock': self.stock,
            'unit': self.unit,
            'category': self.category,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock})"