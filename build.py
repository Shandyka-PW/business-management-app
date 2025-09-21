#!/usr/bin/env python3
"""
Build script for Business Management App
Creates executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    # Dependencies to install
    dependencies = [
        "pyinstaller",
        "pillow",
        "reportlab"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {dep}: {e}")
            return False
    
    return True

def create_icon():
    """Create a simple icon file if not exists"""
    icon_path = "resources/icon.ico"
    
    if not os.path.exists("resources"):
        os.makedirs("resources")
    
    if not os.path.exists(icon_path):
        print("Creating icon file...")
        try:
            # Create a simple icon using PIL
            from PIL import Image, ImageDraw
            
            # Create a simple 256x256 icon
            img = Image.new('RGBA', (256, 256), color=(0, 120, 212, 255))
            draw = ImageDraw.Draw(img)
            
            # Draw a simple business icon
            draw.rectangle([50, 50, 206, 206], fill=(255, 255, 255, 255))
            draw.rectangle([70, 70, 186, 186], fill=(0, 120, 212, 255))
            
            # Add text
            draw.text((90, 110), "BM", fill=(255, 255, 255, 255))
            
            # Save as ICO
            img.save(icon_path, format='ICO')
            print("✓ Icon created successfully")
            
        except ImportError:
            print("⚠ PIL not available, creating placeholder icon")
            # Create a placeholder file
            with open(icon_path, 'w') as f:
                f.write("placeholder")
        except Exception as e:
            print(f"⚠ Could not create icon: {e}")
    
    return icon_path if os.path.exists(icon_path) else None

def build_executable():
    """Build executable using PyInstaller"""
    print("Building executable...")
    
    # Create icon
    icon_path = create_icon()
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=BusinessManagementApp",
        "--onefile",
        "--windowed",
        "--add-data=src;src",
        "--add-data=resources;resources",
        "--clean",
        "--noconfirm"
    ]
    
    # Add icon if available
    if icon_path:
        cmd.extend(["--icon", icon_path])
    
    # Add main script
    cmd.append("main.py")
    
    try:
        # Run PyInstaller
        subprocess.check_call(cmd)
        print("✓ Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def create_installer():
    """Create installer package"""
    print("Creating installer...")
    
    dist_path = "dist"
    if not os.path.exists(dist_path):
        print("✗ Dist directory not found")
        return False
    
    # Get executable path
    exe_path = os.path.join(dist_path, "BusinessManagementApp.exe")
    if not os.path.exists(exe_path):
        print("✗ Executable not found")
        return False
    
    # Create installer directory
    installer_dir = "installer"
    if os.path.exists(installer_dir):
        shutil.rmtree(installer_dir)
    os.makedirs(installer_dir)
    
    # Copy executable
    shutil.copy2(exe_path, installer_dir)
    
    # Create README
    readme_content = """Business Management App - Installer
=====================================

Installation Instructions:
1. Extract all files to a directory
2. Run BusinessManagementApp.exe
3. Follow the license activation prompt

Features:
- Customer Management
- Product Management
- Order Processing
- Financial Tracking
- Invoice Generation
- Database Backup/Restore

System Requirements:
- Windows 7 or later
- 100MB free disk space
- 512MB RAM

Support:
For support, please contact your administrator.

Generated on: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(os.path.join(installer_dir, "README.txt"), "w") as f:
        f.write(readme_content)
    
    # Create batch file for easy installation
    batch_content = """@echo off
echo Business Management App - Installer
echo =====================================
echo.
echo Starting installation...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    echo Please install Python first
    pause
    exit /b 1
)

echo Installation completed successfully!
echo.
echo Starting Business Management App...
start "" "BusinessManagementApp.exe"

pause
"""
    
    with open(os.path.join(installer_dir, "install.bat"), "w") as f:
        f.write(batch_content)
    
    print("✓ Installer package created")
    return True

def cleanup():
    """Clean up build files"""
    print("Cleaning up build files...")
    
    # Directories to remove
    dirs_to_remove = ["build", "__pycache__"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Removed {dir_name}")
    
    # Files to remove
    files_to_remove = ["BusinessManagementApp.spec"]
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✓ Removed {file_name}")

def main():
    """Main build function"""
    print("Business Management App - Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("✗ main.py not found. Please run this script from the project root.")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("✗ Failed to install dependencies")
        return False
    
    # Build executable
    if not build_executable():
        print("✗ Failed to build executable")
        return False
    
    # Create installer
    if not create_installer():
        print("✗ Failed to create installer")
        return False
    
    # Clean up
    cleanup()
    
    print("\n" + "=" * 50)
    print("✓ Build completed successfully!")
    print("Executable location: dist/BusinessManagementApp.exe")
    print("Installer package: installer/")
    print("\nTo distribute the application:")
    print("1. Copy the contents of the 'installer' directory")
    print("2. Distribute to users")
    print("3. Users can run 'install.bat' to start the application")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)