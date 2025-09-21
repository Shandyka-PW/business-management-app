#!/usr/bin/env python3
"""
License Generator for Business Management App
Generate production license keys
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from controllers.license_controller import LicenseController

class LicenseGenerator:
    """License generator for production use"""
    
    def __init__(self):
        self.license_controller = LicenseController()
    
    def generate_license(self, hardware_id, days=365, license_type="standard"):
        """Generate license key for specific hardware"""
        try:
            print(f"Generating license for Hardware ID: {hardware_id}")
            print(f"License Type: {license_type}")
            print(f"Duration: {days} days")
            print("-" * 50)
            
            # Generate license
            license_data = self.license_controller.generate_license_key(hardware_id, days)
            
            if license_data:
                license_key = license_data["license_key"]
                license_info = license_data["license_data"]
                
                print(f"✅ License Key Generated: {license_key}")
                print(f"Created Date: {license_info['created_date']}")
                print(f"Expiry Date: {license_info['expiry_date']}")
                print(f"Type: {license_info['type']}")
                print(f"Version: {license_info['version']}")
                
                # Save license info to file
                self.save_license_info(license_key, license_info, hardware_id)
                
                return license_key
            else:
                print("❌ Failed to generate license")
                return None
                
        except Exception as e:
            print(f"❌ Error generating license: {str(e)}")
            return None
    
    def save_license_info(self, license_key, license_info, hardware_id):
        """Save license information to file"""
        try:
            license_record = {
                "license_key": license_key,
                "hardware_id": hardware_id,
                "generated_date": datetime.now().isoformat(),
                "license_info": license_info
            }
            
            filename = f"licenses/license_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Create licenses directory if not exists
            os.makedirs("licenses", exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump(license_record, f, indent=2)
            
            print(f"📄 License info saved to: {filename}")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not save license info: {str(e)}")
    
    def get_current_hardware_id(self):
        """Get current hardware ID"""
        return self.license_controller.get_hardware_id()
    
    def generate_batch_licenses(self, count=1, days=365):
        """Generate multiple licenses for current hardware"""
        hardware_id = self.get_current_hardware_id()
        licenses = []
        
        for i in range(count):
            license_key = self.generate_license(hardware_id, days)
            if license_key:
                licenses.append(license_key)
        
        return licenses
    
    def validate_license(self, license_key):
        """Validate a license key"""
        is_valid = self.license_controller.validate_license_key(license_key)
        print(f"License '{license_key}' is {'✅ Valid' if is_valid else '❌ Invalid'}")
        return is_valid
    
    def show_license_info(self, license_key):
        """Show detailed license information"""
        license_info = self.license_controller.get_license_info()
        
        if license_info:
            print("\n📋 License Information:")
            print("=" * 50)
            print(f"License Key: {license_info.get('license_key', 'Unknown')}")
            print(f"Hardware ID: {license_info.get('current_hardware_id', 'Unknown')}")
            print(f"Status: {'✅ Valid' if license_info.get('is_valid', False) else '❌ Invalid'}")
            print(f"Saved Date: {license_info.get('saved_date', 'Unknown')}")
            
            if 'license_data' in license_info:
                data = license_info['license_data']
                print(f"Created: {data.get('created_date', 'Unknown')}")
                print(f"Expires: {data.get('expiry_date', 'Unknown')}")
                print(f"Type: {data.get('type', 'Unknown')}")
        else:
            print("❌ No license information found")

def main():
    """Main license generator function"""
    print("Business Management App - License Generator")
    print("=" * 60)
    
    generator = LicenseGenerator()
    
    # Show current hardware ID
    hardware_id = generator.get_current_hardware_id()
    print(f"Current Hardware ID: {hardware_id}")
    print()
    
    while True:
        print("\n📋 License Generator Menu:")
        print("1. Generate Single License")
        print("2. Generate Multiple Licenses")
        print("3. Validate License Key")
        print("4. Show Current License Info")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            # Generate single license
            print("\n🔑 Generate Single License")
            print("-" * 30)
            
            hardware_input = input(f"Enter Hardware ID [{hardware_id}]: ").strip()
            if not hardware_input:
                hardware_input = hardware_id
            
            try:
                days = int(input("Enter license duration in days [365]: ") or "365")
                license_type = input("Enter license type [standard]: ").strip() or "standard"
                
                license_key = generator.generate_license(hardware_input, days, license_type)
                if license_key:
                    print(f"\n✅ License generated successfully!")
                    print(f"📝 License Key: {license_key}")
                    print(f"🔒 Hardware ID: {hardware_input}")
                    print(f"⏰ Valid for: {days} days")
            except ValueError:
                print("❌ Invalid input for days")
        
        elif choice == "2":
            # Generate multiple licenses
            print("\n🔑 Generate Multiple Licenses")
            print("-" * 35)
            
            try:
                count = int(input("Enter number of licenses to generate: "))
                days = int(input("Enter license duration in days [365]: ") or "365")
                
                licenses = generator.generate_batch_licenses(count, days)
                if licenses:
                    print(f"\n✅ Generated {len(licenses)} licenses:")
                    for i, key in enumerate(licenses, 1):
                        print(f"{i}. {key}")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == "3":
            # Validate license
            print("\n✅ Validate License")
            print("-" * 20)
            
            license_key = input("Enter license key to validate: ").strip()
            if license_key:
                generator.validate_license(license_key)
            else:
                print("❌ Please enter a license key")
        
        elif choice == "4":
            # Show current license info
            print("\n📋 Current License Information")
            print("-" * 35)
            generator.show_license_info("")
        
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()