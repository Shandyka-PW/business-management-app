"""
Fixed License Controller for Business Management App
Handles license validation and management with safe imports
"""

import hashlib
import json
import os
from datetime import datetime, timedelta

# Safe imports for built-in modules that might not be available in PyInstaller bundle
try:
    import platform
    HAS_PLATFORM = True
except ImportError:
    HAS_PLATFORM = False
    print("Warning: platform module not available")

try:
    import uuid
    HAS_UUID = True
except ImportError:
    HAS_UUID = False
    print("Warning: uuid module not available")

try:
    import winreg
    HAS_WINREG = True
except ImportError:
    HAS_WINREG = False
    print("Warning: winreg module not available")

from utils.config import Config

class LicenseController:
    """Controller for managing software licenses"""
    
    def __init__(self):
        self.config = Config()
        self.license_file = os.path.join(self.config.get_app_data_dir(), "license.json")
    
    def get_hardware_id(self):
        """Generate unique hardware ID based on system components"""
        try:
            # Get machine UUID
            if HAS_UUID:
                machine_uuid = str(uuid.getnode())
            else:
                # Fallback: use random number
                import random
                machine_uuid = str(random.randint(100000000000000, 999999999999999))
            
            # Get processor info
            processor_info = ""
            if HAS_PLATFORM:
                try:
                    if HAS_WINREG and platform.system() == "Windows":
                        try:
                            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                               r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                            processor_info = winreg.QueryValueEx(key, "ProcessorNameString")[0]
                            winreg.CloseKey(key)
                        except:
                            processor_info = platform.processor()
                    else:
                        processor_info = platform.processor()
                except:
                    processor_info = "Unknown Processor"
            else:
                processor_info = "Unknown Processor"
            
            # Get system info
            if HAS_PLATFORM:
                try:
                    system_info = f"{platform.system()} {platform.release()} {platform.machine()}"
                except:
                    system_info = "Unknown System"
            else:
                system_info = "Unknown System"
            
            # Combine all info and create hash
            combined_info = f"{machine_uuid}{processor_info}{system_info}"
            hardware_id = hashlib.sha256(combined_info.encode()).hexdigest()[:16]
            
            return hardware_id.upper()
        except Exception as e:
            print(f"Error getting hardware ID: {e}")
            # Fallback to random UUID
            if HAS_UUID:
                return str(uuid.uuid4()).replace('-', '')[:16].upper()
            else:
                import random
                return ''.join([random.choice('0123456789ABCDEF') for _ in range(16)])
    
    def generate_license_key(self, hardware_id, days=365):
        """Generate license key for specific hardware"""
        try:
            # Create license data
            license_data = {
                "hardware_id": hardware_id,
                "created_date": datetime.now().isoformat(),
                "expiry_date": (datetime.now() + timedelta(days=days)).isoformat(),
                "type": "standard",
                "version": "1.0"
            }
            
            # Create signature (simplified - in production use proper encryption)
            signature_data = f"{hardware_id}{license_data['created_date']}{license_data['expiry_date']}"
            signature = hashlib.sha256(signature_data.encode()).hexdigest()
            
            # Create license key format: XXXX-XXXX-XXXX-XXXX
            license_key = f"{signature[:4]}-{signature[4:8]}-{signature[8:12]}-{signature[12:16]}".upper()
            
            return {
                "license_key": license_key,
                "license_data": license_data
            }
        except Exception as e:
            print(f"Error generating license: {e}")
            return None
    
    def validate_license_key(self, license_key):
        """Validate license key for current hardware"""
        try:
            if not license_key or len(license_key) != 19:  # XXXX-XXXX-XXXX-XXXX
                return False
            
            # Get current hardware ID
            current_hardware_id = self.get_hardware_id()
            
            # Remove dashes and convert to lowercase for processing
            clean_key = license_key.replace('-', '').lower()
            
            # Recreate signature
            signature_data = f"{current_hardware_id}"
            expected_signature = hashlib.sha256(signature_data.encode()).hexdigest()
            
            # Check if key matches expected format (simplified validation)
            if clean_key == expected_signature[:16]:
                return True
            
            # For demo purposes, accept some predefined keys
            demo_keys = [
                "DEMO-KEY-1234-5678",
                "BUSINESS-APP-2024-PRO",
                "PREMIUM-LIFETIME-2024",
                "TEST-DEV-2024-KEY",
                "EDUCATION-FREE-2024",
                "ENTERPRISE-BUS-2024"
            ]
            
            return license_key in demo_keys
            
        except Exception as e:
            print(f"Error validating license: {e}")
            return False
    
    def save_license(self, license_key, license_data=None):
        """Save license to file"""
        try:
            license_info = {
                "license_key": license_key,
                "saved_date": datetime.now().isoformat(),
                "hardware_id": self.get_hardware_id()
            }
            
            if license_data:
                license_info.update(license_data)
            
            with open(self.license_file, 'w') as f:
                json.dump(license_info, f, indent=2)
            
            # Also save to config
            self.config.set("license_key", license_key)
            
            return True
        except Exception as e:
            print(f"Error saving license: {e}")
            return False
    
    def load_license(self):
        """Load license from file"""
        try:
            if os.path.exists(self.license_file):
                with open(self.license_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading license: {e}")
            return None
    
    def is_licensed(self):
        """Check if application is licensed"""
        try:
            # First check config
            license_key = self.config.get("license_key")
            if license_key and self.validate_license_key(license_key):
                return True
            
            # Then check license file
            license_info = self.load_license()
            if license_info and "license_key" in license_info:
                if self.validate_license_key(license_info["license_key"]):
                    return True
            
            return False
        except Exception as e:
            print(f"Error checking license: {e}")
            return False
    
    def remove_license(self):
        """Remove license (for testing or transfer)"""
        try:
            if os.path.exists(self.license_file):
                os.remove(self.license_file)
            
            self.config.set("license_key", "")
            return True
        except Exception as e:
            print(f"Error removing license: {e}")
            return False
    
    def get_license_info(self):
        """Get license information"""
        license_info = self.load_license()
        if not license_info:
            return None
        
        # Add validation status
        license_info["is_valid"] = self.validate_license_key(license_info.get("license_key", ""))
        license_info["current_hardware_id"] = self.get_hardware_id()
        
        return license_info
    
    def create_demo_license(self):
        """Create a demo license for testing"""
        hardware_id = self.get_hardware_id()
        demo_key = "DEMO-KEY-1234-5678"
        
        license_data = {
            "hardware_id": hardware_id,
            "created_date": datetime.now().isoformat(),
            "expiry_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "type": "demo",
            "version": "1.0"
        }
        
        if self.save_license(demo_key, license_data):
            return demo_key
        return None