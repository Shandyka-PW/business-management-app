"""
Configuration utilities for Business Management App
"""

import os
import json
import platform
from pathlib import Path

class Config:
    """Configuration management class"""
    
    def __init__(self):
        self.config_file = "config.json"
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "app_name": "Business Management App",
            "version": "1.0.0",
            "database_path": "database/business.db",
            "backup_path": "backup",
            "license_key": "",
            "company_info": {
                "name": "Your Company",
                "address": "Company Address",
                "phone": "Company Phone",
                "email": "company@email.com"
            },
            "settings": {
                "auto_backup": True,
                "backup_interval_days": 7,
                "currency": "IDR",
                "language": "id"
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with default config to ensure all keys exist
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                print(f"Error loading config: {e}")
                return default_config
        else:
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    def get_app_data_dir(self):
        """Get application data directory"""
        if platform.system() == "Windows":
            app_data = os.path.expandvars("%APPDATA%")
        else:
            app_data = os.path.expanduser("~")
        
        app_dir = os.path.join(app_data, "BusinessManagementApp")
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        
        return app_dir
    
    def get_database_path(self):
        """Get database file path"""
        db_path = self.get("database_path")
        if not os.path.isabs(db_path):
            db_path = os.path.join(self.get_app_data_dir(), os.path.basename(db_path))
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        return db_path
    
    def get_backup_path(self):
        """Get backup directory path"""
        backup_path = self.get("backup_path")
        if not os.path.isabs(backup_path):
            backup_path = os.path.join(self.get_app_data_dir(), "backup")
        
        # Ensure directory exists
        os.makedirs(backup_path, exist_ok=True)
        
        return backup_path