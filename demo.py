#!/usr/bin/env python3
"""
Demo script for Business Management App
Creates sample data and demonstrates app functionality
"""

import os
import sys
from datetime import datetime, timedelta

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from controllers.database_controller import DatabaseController
from controllers.license_controller import LicenseController
from models.customer import Customer
from models.product import Product
from models.order import Order

def create_sample_data():
    """Create sample data for demonstration"""
    print("Creating sample data...")
    
    # Initialize database
    db = DatabaseController()
    db.initialize_database()
    
    # Create sample customers
    customers_data = [
        {
            "name": "PT. Maju Bersama",
            "phone": "+62 21 5555 1234",
            "email": "info@majubersama.com",
            "address": "Jl. Sudirman No. 123, Jakarta"
        },
        {
            "name": "CV. Sukses Jaya",
            "phone": "+62 22 6666 5678",
            "email": "contact@suksesjaya.com",
            "address": "Jl. Thamrin No. 456, Bandung"
        },
        {
            "name": "UD. Makmur Sentosa",
            "phone": "+62 31 7777 9012",
            "email": "udmakmur@email.com",
            "address": "Jl. Tunjungan No. 789, Surabaya"
        },
        {
            "name": "Budi Santoso",
            "phone": "+62 812 3456 7890",
            "email": "budi.santoso@email.com",
            "address": "Perumahan Indah Blok A No. 12"
        },
        {
            "name": "Siti Nurhaliza",
            "phone": "+62 813 5678 9012",
            "email": "siti.nurhaliza@email.com",
            "address": "Jl. Merdeka No. 234"
        }
    ]
    
    customers = []
    for data in customers_data:
        customer = Customer(**data)
        customer.save()
        customers.append(customer)
        print(f"✓ Created customer: {customer.name}")
    
    # Create sample products
    products_data = [
        {
            "name": "Laptop ASUS ROG",
            "description": "Laptop gaming high performance",
            "price": 15000000,
            "cost": 12000000,
            "stock": 10,
            "unit": "unit",
            "category": "Elektronik"
        },
        {
            "name": "Mouse Gaming Logitech",
            "description": "Mouse gaming dengan RGB",
            "price": 500000,
            "cost": 350000,
            "stock": 25,
            "unit": "unit",
            "category": "Elektronik"
        },
        {
            "name": "Keyboard Mechanical",
            "description": "Keyboard mechanical switch blue",
            "price": 800000,
            "cost": 550000,
            "stock": 15,
            "unit": "unit",
            "category": "Elektronik"
        },
        {
            "name": "Monitor LG 24 inch",
            "description": "Monitor LED 24 inch Full HD",
            "price": 2500000,
            "cost": 1800000,
            "stock": 8,
            "unit": "unit",
            "category": "Elektronik"
        },
        {
            "name": "Printer Epson L3210",
            "description": "Printer infus multifungsi",
            "price": 3500000,
            "cost": 2800000,
            "stock": 5,
            "unit": "unit",
            "category": "Elektronik"
        },
        {
            "name": "Kemeja Batik Premium",
            "description": "Kemeja batik premium katun",
            "price": 350000,
            "cost": 200000,
            "stock": 30,
            "unit": "pcs",
            "category": "Fashion"
        },
        {
            "name": "Sepatu Sneakers",
            "description": "Sepatu sneakers casual",
            "price": 450000,
            "cost": 300000,
            "stock": 20,
            "unit": "pair",
            "category": "Fashion"
        },
        {
            "name": "Tas Ransel",
            "description": "Tas ransel laptop 15 inch",
            "price": 300000,
            "cost": 200000,
            "stock": 12,
            "unit": "unit",
            "category": "Fashion"
        }
    ]
    
    products = []
    for data in products_data:
        product = Product(**data)
        product.save()
        products.append(product)
        print(f"✓ Created product: {product.name}")
    
    # Create sample orders
    orders_data = [
        {
            "customer_id": customers[0].id,
            "status": "paid",
            "notes": "Order untuk kantor baru"
        },
        {
            "customer_id": customers[1].id,
            "status": "pending",
            "notes": "Menunggu konfirmasi pembayaran"
        },
        {
            "customer_id": customers[3].id,
            "status": "paid",
            "notes": "Pembelian personal"
        },
        {
            "customer_id": customers[2].id,
            "status": "unpaid",
            "notes": "Pembayaran tempo 30 hari"
        },
        {
            "customer_id": customers[4].id,
            "status": "paid",
            "notes": "Order repeat customer"
        }
    ]
    
    orders = []
    for i, data in enumerate(orders_data):
        order = Order(**data)
        order.save()
        orders.append(order)
        
        # Add items to order
        if i == 0:  # First order - multiple items
            order.add_item(products[0].id, 2, products[0].price)  # 2 laptops
            order.add_item(products[1].id, 5, products[1].price)  # 5 mice
            order.add_item(products[2].id, 3, products[2].price)  # 3 keyboards
            order.add_payment(order.total_amount, "transfer")
        elif i == 1:  # Second order - monitors
            order.add_item(products[3].id, 4, products[3].price)  # 4 monitors
            order.add_payment(order.total_amount * 0.5, "cash")  # Partial payment
        elif i == 2:  # Third order - fashion items
            order.add_item(products[5].id, 3, products[5].price)  # 3 shirts
            order.add_item(products[7].id, 1, products[7].price)  # 1 backpack
            order.add_payment(order.total_amount, "cash")
        elif i == 3:  # Fourth order - printer
            order.add_item(products[4].id, 2, products[4].price)  # 2 printers
            # No payment - unpaid
        elif i == 4:  # Fifth order - sneakers
            order.add_item(products[6].id, 2, products[6].price)  # 2 pairs of sneakers
            order.add_payment(order.total_amount, "transfer")
        
        print(f"✓ Created order: {order.order_number} - Total: Rp {order.total_amount:,.0f}")
    
    # Update company settings
    db.set_setting("company_name", "PT. Demo Business Indonesia", "Nama perusahaan demo")
    db.set_setting("company_address", "Jl. Demo No. 123, Jakarta 12345", "Alamat perusahaan")
    db.set_setting("company_phone", "+62 21 1234 5678", "Telepon perusahaan")
    db.set_setting("company_email", "info@demobusiness.com", "Email perusahaan")
    
    print("\n✓ Sample data created successfully!")
    print(f"Created {len(customers)} customers")
    print(f"Created {len(products)} products")
    print(f"Created {len(orders)} orders")
    
    return True

def activate_demo_license():
    """Activate demo license"""
    print("Activating demo license...")
    
    license_controller = LicenseController()
    demo_key = license_controller.create_demo_license()
    
    if demo_key:
        print(f"✓ Demo license activated: {demo_key}")
        print("License valid for 30 days")
        return True
    else:
        print("✗ Failed to activate demo license")
        return False

def show_database_info():
    """Show database information"""
    print("\nDatabase Information:")
    print("=" * 50)
    
    db = DatabaseController()
    info = db.get_database_info()
    
    if info:
        print(f"Database path: {info['database_path']}")
        print(f"Database size: {info['database_size']} bytes")
        print("\nTable records:")
        for table, count in info['tables'].items():
            print(f"  {table}: {count} records")
    
    print("\n" + "=" * 50)

def main():
    """Main demo function"""
    print("Business Management App - Demo Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("✗ main.py not found. Please run this script from the project root.")
        return False
    
    try:
        # Activate demo license
        if not activate_demo_license():
            print("✗ Demo setup failed")
            return False
        
        # Create sample data
        if not create_sample_data():
            print("✗ Sample data creation failed")
            return False
        
        # Show database info
        show_database_info()
        
        print("\n" + "=" * 50)
        print("✓ Demo setup completed successfully!")
        print("\nNext steps:")
        print("1. Run 'python main.py' to start the application")
        print("2. Use demo license: DEMO-KEY-1234-5678")
        print("3. Explore all features with sample data")
        print("\nNote: This demo creates sample data for testing purposes.")
        print("You can delete and recreate data as needed.")
        
        return True
        
    except Exception as e:
        print(f"✗ Demo setup failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)