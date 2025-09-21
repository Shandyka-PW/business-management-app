#!/usr/bin/env python3
"""
Business Management App - Fixed Version
Author: AI Assistant
Version: 1.0.0
"""

import sys
import os
import logging
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import fixed license controller
from controllers.license_controller_fixed import LicenseController
from controllers.database_controller import DatabaseController
from views.main_window import MainWindow
from utils.config import Config

def setup_logging():
    """Setup logging untuk aplikasi"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"business_app_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def main():
    """Main function untuk menjalankan aplikasi"""
    logger = setup_logging()
    logger.info("Starting Business Management App (Fixed Version)")
    
    try:
        # Inisialisasi config
        config = Config()
        
        # Cek lisensi
        license_controller = LicenseController()
        if not license_controller.is_licensed():
            logger.info("Application not licensed, showing license dialog")
            from views.license_dialog import LicenseDialog
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # Hide main window temporarily
            
            license_dialog = LicenseDialog(root)
            if not license_dialog.show():
                logger.error("License validation failed")
                return
        
        # Inisialisasi database
        db_controller = DatabaseController()
        db_controller.initialize_database()
        
        # Jalankan aplikasi utama
        app = MainWindow()
        app.run()
        
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"Gagal menjalankan aplikasi: {str(e)}")

if __name__ == "__main__":
    main()