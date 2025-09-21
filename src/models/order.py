"""
Order Model for Business Management App
"""

from datetime import datetime, timedelta
from controllers.database_controller import DatabaseController
from models.customer import Customer
from models.product import Product

class Order:
    """Order model class"""
    
    def __init__(self, id=None, order_number=None, customer_id=None, order_date=None, 
                 due_date=None, status='pending', total_amount=0, paid_amount=0, notes=None):
        self.id = id
        self.order_number = order_number
        self.customer_id = customer_id
        self.order_date = order_date
        self.due_date = due_date
        self.status = status
        self.total_amount = total_amount
        self.paid_amount = paid_amount
        self.notes = notes
        self.created_at = None
        self.updated_at = None
        self.db = DatabaseController()
        self.items = []
    
    def save(self):
        """Save order to database"""
        try:
            if self.id is None:
                # Generate order number if not exists
                if not self.order_number:
                    self.order_number = self.db.generate_number('ORD', 'orders', 'order_number')
                
                # Insert new order
                query = '''
                    INSERT INTO orders (order_number, customer_id, order_date, due_date, 
                                     status, total_amount, paid_amount, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                '''
                params = (self.order_number, self.customer_id, self.order_date, self.due_date,
                         self.status, self.total_amount, self.paid_amount, self.notes)
                self.id = self.db.execute_query(query, params)
            else:
                # Update existing order
                query = '''
                    UPDATE orders 
                    SET order_number = ?, customer_id = ?, order_date = ?, due_date = ?,
                        status = ?, total_amount = ?, paid_amount = ?, notes = ?, 
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                '''
                params = (self.order_number, self.customer_id, self.order_date, self.due_date,
                         self.status, self.total_amount, self.paid_amount, self.notes, self.id)
                self.db.execute_query(query, params)
            
            return True
        except Exception as e:
            print(f"Error saving order: {e}")
            return False
    
    def delete(self):
        """Delete order from database"""
        try:
            if self.id is None:
                return False
            
            # Delete order items first
            query = "DELETE FROM order_items WHERE order_id = ?"
            self.db.execute_query(query, (self.id,))
            
            # Delete order
            query = "DELETE FROM orders WHERE id = ?"
            self.db.execute_query(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting order: {e}")
            return False
    
    def add_item(self, product_id, quantity, price):
        """Add item to order"""
        try:
            if self.id is None:
                return False
            
            total = quantity * price
            
            query = '''
                INSERT INTO order_items (order_id, product_id, quantity, price, total)
                VALUES (?, ?, ?, ?, ?)
            '''
            params = (self.id, product_id, quantity, price, total)
            item_id = self.db.execute_query(query, params)
            
            # Update order total
            self.update_total()
            
            # Update product stock
            product = Product.get_by_id(product_id)
            if product:
                product.update_stock(-quantity)
            
            return item_id
        except Exception as e:
            print(f"Error adding order item: {e}")
            return False
    
    def remove_item(self, item_id):
        """Remove item from order"""
        try:
            if self.id is None:
                return False
            
            # Get item details
            query = "SELECT * FROM order_items WHERE id = ?"
            result = self.db.execute_query(query, (item_id,))
            
            if result:
                item = result[0]
                
                # Restore product stock
                product = Product.get_by_id(item['product_id'])
                if product:
                    product.update_stock(item['quantity'])
                
                # Delete item
                query = "DELETE FROM order_items WHERE id = ?"
                self.db.execute_query(query, (item_id,))
                
                # Update order total
                self.update_total()
                
                return True
            
            return False
        except Exception as e:
            print(f"Error removing order item: {e}")
            return False
    
    def update_total(self):
        """Update order total amount"""
        try:
            if self.id is None:
                return False
            
            query = "SELECT COALESCE(SUM(total), 0) as total FROM order_items WHERE order_id = ?"
            result = self.db.execute_query(query, (self.id,))
            
            if result:
                total = result[0]['total']
                self.total_amount = total
                
                query = "UPDATE orders SET total_amount = ? WHERE id = ?"
                self.db.execute_query(query, (total, self.id))
                
                return True
            
            return False
        except Exception as e:
            print(f"Error updating order total: {e}")
            return False
    
    def add_payment(self, amount, payment_method='cash'):
        """Add payment to order"""
        try:
            if self.id is None:
                return False
            
            new_paid_amount = self.paid_amount + amount
            query = "UPDATE orders SET paid_amount = ? WHERE id = ?"
            self.db.execute_query(query, (new_paid_amount, self.id))
            
            self.paid_amount = new_paid_amount
            
            # Update status if fully paid
            if self.paid_amount >= self.total_amount:
                self.status = 'paid'
                query = "UPDATE orders SET status = ? WHERE id = ?"
                self.db.execute_query(query, (self.status, self.id))
            
            # Record financial transaction
            self.record_payment(amount, payment_method)
            
            return True
        except Exception as e:
            print(f"Error adding payment: {e}")
            return False
    
    def record_payment(self, amount, payment_method):
        """Record payment transaction"""
        try:
            query = '''
                INSERT INTO financial_transactions (type, category, amount, description, 
                                                  date, reference_id, reference_type, payment_method)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = ('income', 'payment', amount, f'Payment for order {self.order_number}',
                     datetime.now(), str(self.id), 'order', payment_method)
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error recording payment: {e}")
            return False
    
    def get_items(self):
        """Get order items"""
        try:
            if self.id is None:
                return []
            
            query = '''
                SELECT oi.*, p.name as product_name, p.unit as product_unit
                FROM order_items oi
                LEFT JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = ?
                ORDER BY oi.id
            '''
            results = self.db.execute_query(query, (self.id,))
            return results
        except Exception as e:
            print(f"Error getting order items: {e}")
            return []
    
    def get_customer(self):
        """Get order customer"""
        try:
            if self.customer_id:
                return Customer.get_by_id(self.customer_id)
            return None
        except Exception as e:
            print(f"Error getting order customer: {e}")
            return None
    
    @classmethod
    def get_by_id(cls, order_id):
        """Get order by ID"""
        try:
            db = DatabaseController()
            query = "SELECT * FROM orders WHERE id = ?"
            result = db.execute_query(query, (order_id,))
            
            if result:
                data = result[0]
                order = cls(
                    id=data['id'],
                    order_number=data['order_number'],
                    customer_id=data['customer_id'],
                    order_date=data['order_date'],
                    due_date=data['due_date'],
                    status=data['status'],
                    total_amount=data['total_amount'],
                    paid_amount=data['paid_amount'],
                    notes=data['notes']
                )
                order.created_at = data['created_at']
                order.updated_at = data['updated_at']
                return order
            return None
        except Exception as e:
            print(f"Error getting order: {e}")
            return None
    
    @classmethod
    def get_by_number(cls, order_number):
        """Get order by order number"""
        try:
            db = DatabaseController()
            query = "SELECT * FROM orders WHERE order_number = ?"
            result = db.execute_query(query, (order_number,))
            
            if result:
                data = result[0]
                order = cls(
                    id=data['id'],
                    order_number=data['order_number'],
                    customer_id=data['customer_id'],
                    order_date=data['order_date'],
                    due_date=data['due_date'],
                    status=data['status'],
                    total_amount=data['total_amount'],
                    paid_amount=data['paid_amount'],
                    notes=data['notes']
                )
                order.created_at = data['created_at']
                order.updated_at = data['updated_at']
                return order
            return None
        except Exception as e:
            print(f"Error getting order: {e}")
            return None
    
    @classmethod
    def get_all(cls):
        """Get all orders"""
        try:
            db = DatabaseController()
            query = "SELECT * FROM orders ORDER BY order_date DESC"
            results = db.execute_query(query)
            
            orders = []
            for data in results:
                order = cls(
                    id=data['id'],
                    order_number=data['order_number'],
                    customer_id=data['customer_id'],
                    order_date=data['order_date'],
                    due_date=data['due_date'],
                    status=data['status'],
                    total_amount=data['total_amount'],
                    paid_amount=data['paid_amount'],
                    notes=data['notes']
                )
                order.created_at = data['created_at']
                order.updated_at = data['updated_at']
                orders.append(order)
            
            return orders
        except Exception as e:
            print(f"Error getting orders: {e}")
            return []
    
    @classmethod
    def get_by_status(cls, status):
        """Get orders by status"""
        try:
            db = DatabaseController()
            query = "SELECT * FROM orders WHERE status = ? ORDER BY order_date DESC"
            results = db.execute_query(query, (status,))
            
            orders = []
            for data in results:
                order = cls(
                    id=data['id'],
                    order_number=data['order_number'],
                    customer_id=data['customer_id'],
                    order_date=data['order_date'],
                    due_date=data['due_date'],
                    status=data['status'],
                    total_amount=data['total_amount'],
                    paid_amount=data['paid_amount'],
                    notes=data['notes']
                )
                order.created_at = data['created_at']
                order.updated_at = data['updated_at']
                orders.append(order)
            
            return orders
        except Exception as e:
            print(f"Error getting orders by status: {e}")
            return []
    
    @classmethod
    def get_unpaid(cls):
        """Get unpaid orders"""
        try:
            db = DatabaseController()
            query = '''
                SELECT * FROM orders 
                WHERE paid_amount < total_amount 
                ORDER BY order_date DESC
            '''
            results = db.execute_query(query)
            
            orders = []
            for data in results:
                order = cls(
                    id=data['id'],
                    order_number=data['order_number'],
                    customer_id=data['customer_id'],
                    order_date=data['order_date'],
                    due_date=data['due_date'],
                    status=data['status'],
                    total_amount=data['total_amount'],
                    paid_amount=data['paid_amount'],
                    notes=data['notes']
                )
                order.created_at = data['created_at']
                order.updated_at = data['updated_at']
                orders.append(order)
            
            return orders
        except Exception as e:
            print(f"Error getting unpaid orders: {e}")
            return []
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_id': self.customer_id,
            'order_date': self.order_date,
            'due_date': self.due_date,
            'status': self.status,
            'total_amount': self.total_amount,
            'paid_amount': self.paid_amount,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'remaining_amount': self.total_amount - self.paid_amount
        }
    
    def __str__(self):
        return f"Order(id={self.id}, number='{self.order_number}', status='{self.status}')"