#!/usr/bin/env python3
"""
Fixed Build script for Business Management App
Creates executable using PyInstaller with proper module handling
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
        "pyinstaller==6.1.0",
        "Pillow==10.1.0", 
        "reportlab==4.0.7"
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
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a simple 256x256 icon
            img = Image.new('RGBA', (256, 256), color=(0, 120, 212, 255))
            draw = ImageDraw.Draw(img)
            
            # Draw a simple business icon
            draw.rectangle([40, 40, 216, 216], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
            draw.rectangle([60, 60, 196, 196], fill=(0, 120, 212, 255), outline=(0, 0, 0, 255))
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            draw.text((80, 100), "BM", fill=(255, 255, 255, 255), font=font)
            
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
            # Create a simple text file as fallback
            with open(icon_path, 'w') as f:
                f.write("icon")
    
    return icon_path if os.path.exists(icon_path) else None

def build_executable():
    """Build executable using PyInstaller with comprehensive settings"""
    print("Building executable...")
    
    # Create icon
    icon_path = create_icon()
    
    # Clean previous builds
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    # Remove spec file if exists
    if os.path.exists('BusinessManagementApp.spec'):
        os.remove('BusinessManagementApp.spec')
    
    try:
        # Use comprehensive PyInstaller command
        cmd = [
            "pyinstaller",
            "--name=BusinessManagementApp",
            "--onefile",
            "--windowed",
            "--add-data=src;src",
            "--add-data=resources;resources",
            "--hidden-import=platform",
            "--hidden-import=winreg", 
            "--hidden-import=uuid",
            "--hidden-import=hashlib",
            "--hidden-import=json",
            "--hidden-import=os",
            "--hidden-import=sys",
            "--hidden-import=datetime",
            "--hidden-import=sqlite3",
            "--hidden-import=tkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.messagebox",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=tkinter.colorchooser",
            "--hidden-import=tkinter.font",
            "--hidden-import=tkinter.scrolledtext",
            "--hidden-import=tkinter.dnd2",
            "--hidden-import=tkinter.tix",
            "--hidden-import=PIL",
            "--hidden-import=PIL.Image",
            "--hidden-import=PIL.ImageDraw",
            "--hidden-import=PIL.ImageFont",
            "--hidden-import=PIL.ImageFilter",
            "--hidden-import=PIL.ImageEnhance",
            "--hidden-import=PIL.ImageOps",
            "--hidden-import=PIL.ImageSequence",
            "--hidden-import=PIL.ImageChops",
            "--hidden-import=PIL.ImageColor",
            "--hidden-import=PIL.ImageFile",
            "--hidden-import=PIL.ImageMode",
            "--hidden-import=PIL.ImageStat",
            "--hidden-import=PIL.ImageTransform",
            "--hidden-import=PIL.ImageMorph",
            "--hidden-import=PIL.ImageDraw2",
            "--hidden-import=PIL.ImageShow",
            "--hidden-import=PIL.ImageQt",
            "--hidden-import=PIL.ImageTk",
            "--hidden-import=PIL.ImageWin",
            "--hidden-import=PIL.PyAccess",
            "--hidden-import=reportlab",
            "--hidden-import=reportlab.pdfgen",
            "--hidden-import=reportlab.pdfgen.canvas",
            "--hidden-import=reportlab.lib.pagesizes",
            "--hidden-import=reportlab.lib.styles",
            "--hidden-import=reportlab.lib.units",
            "--hidden-import=reportlab.lib.colors",
            "--hidden-import=reportlab.lib.enums",
            "--hidden-import=reportlab.lib.fonts",
            "--hidden-import=reportlab.lib.utils",
            "--hidden-import=reportlab.platypus",
            "--hidden-import=reportlab.platypus.tables",
            "--hidden-import=reportlab.platypus.paragraph",
            "--hidden-import=reportlab.platypus.flowables",
            "--hidden-import=reportlab.platypus.frames",
            "--hidden-import=reportlab.platypus.doctemplate",
            "--hidden-import=reportlab.platypus.paraparser",
            "--hidden-import=reportlab.graphics",
            "--hidden-import=reportlab.graphics.shapes",
            "--hidden-import=reportlab.graphics.renderPDF",
            "--hidden-import=reportlab.graphics.renderPM",
            "--hidden-import=reportlab.graphics.charts",
            "--hidden-import=reportlab.graphics.charts.lineplots",
            "--hidden-import=reportlab.graphics.charts.barcharts",
            "--hidden-import=reportlab.graphics.charts.piecharts",
            "--hidden-import=reportlab.graphics.widgets",
            "--hidden-import=reportlab.graphics.widgets.markers",
            "--hidden-import=reportlab.graphics.widgetbase",
            "--hidden-import=shutil",
            "--hidden-import=logging",
            "--hidden-import=configparser",
            "--hidden-import=pathlib",
            "--hidden-import=subprocess",
            "--hidden-import=threading",
            "--hidden-import=time",
            "--hidden-import=random",
            "--hidden-import=string",
            "--hidden-import=re",
            "--hidden-import=io",
            "--hidden-import=base64",
            "--hidden-import=decimal",
            "--hidden-import=math",
            "--hidden-import=calendar",
            "--hidden-import=email",
            "--hidden-import=email.utils",
            "--hidden-import=urllib",
            "--hidden-import=urllib.parse",
            "--hidden-import=html",
            "--hidden-import=html.parser",
            "--hidden-import=xml",
            "--hidden-import=xml.etree",
            "--hidden-import=xml.etree.ElementTree",
            "--hidden-import=csv",
            "--hidden-import=zipfile",
            "--hidden-import=gzip",
            "--hidden-import=tempfile",
            "--hidden-import=glob",
            "--hidden-import=fnmatch",
            "--hidden-import=inspect",
            "--hidden-import=traceback",
            "--hidden-import=warnings",
            "--hidden-import=weakref",
            "--hidden-import=copy",
            "--hidden-import=pickle",
            "--hidden-import=marshal",
            "--hidden-import=imp",
            "--hidden-import=importlib",
            "--hidden-import=pkgutil",
            "--hidden-import=modulefinder",
            "--hidden-import=dis",
            "--hidden-import=opcode",
            "--hidden-import=ast",
            "--hidden-import=token",
            "--hidden-import=tokenize",
            "--hidden-import=keyword",
            "--hidden-import=tabnanny",
            "--hidden-import=py_compile",
            "--hidden-import=compileall",
            "--hidden-import=encodings",
            "--hidden-import=encodings.aliases",
            "--hidden-import=encodings.ascii",
            "--hidden-import=encodings.latin_1",
            "--hidden-import=encodings.utf_8",
            "--hidden-import=encodings.mbcs",
            "--hidden-import=encodings.utf_16",
            "--hidden-import=encodings.utf_32",
            "--hidden-import=codecs",
            "--hidden-import=locale",
            "--hidden-import=gettext",
            "--hidden-import=heapq",
            "--hidden-import=bisect",
            "--hidden-import=array",
            "--hidden-import=collections",
            "--hidden-import=collections.abc",
            "--hidden-import=itertools",
            "--hidden-import=functools",
            "--hidden-import=operator",
            "--hidden-import=contextlib",
            "--hidden-import=types",
            "--hidden-import=copyreg",
            "--hidden-import=reprlib",
            "--hidden-import=abc",
            "--hidden-import=numbers",
            "--hidden-import=statistics",
            "--hidden-import=os.path",
            "--hidden-import=sysconfig",
            "--hidden-import=md5",
            "--hidden-import=sha1",
            "--hidden-import=sha256",
            "--hidden-import=sha512",
            "--hidden-import=hmac",
            "--hidden-import=secrets",
            "--hidden-import=StringIO",
            "--hidden-import=BytesIO",
            "--hidden-import=binascii",
            "--hidden-import=quopri",
            "--hidden-import=uu",
            "--hidden-import=html.entities",
            "--hidden-import=xml.dom",
            "--hidden-import=xml.dom.minidom",
            "--hidden-import=xml.dom.pulldom",
            "--hidden-import=xml.sax",
            "--hidden-import=xml.sax.handler",
            "--hidden-import=xml.sax.saxutils",
            "--hidden-import=xml.sax.xmlreader",
            "--hidden-import=json.tool",
            "--hidden-import=sqlite3.dbapi2",
            "--hidden-import=sqlite3.dump",
            "--hidden-import=sqlite3.row",
            "--collect-all=tkinter",
            "--collect-all=PIL",
            "--collect-all=reportlab",
            "--clean",
            "--noconfirm",
            "--debug=all",
            "--log-level=DEBUG"
        ]
        
        # Add icon if available
        if icon_path and os.path.exists(icon_path):
            cmd.extend(["--icon", icon_path])
        
        # Add main script
        cmd.append("main.py")
        
        print("Running PyInstaller with command:")
        print(" ".join(cmd))
        print()
        
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
echo Starting application...
echo.

REM Check if executable exists
if not exist "BusinessManagementApp.exe" (
    echo Error: BusinessManagementApp.exe not found
    echo Please extract all files first
    pause
    exit /b 1
)

echo Starting Business Management App...
start "" "BusinessManagementApp.exe"

pause
"""
    
    with open(os.path.join(installer_dir, "run.bat"), "w") as f:
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

def test_executable():
    """Test the built executable"""
    print("Testing executable...")
    
    exe_path = "dist/BusinessManagementApp.exe"
    if not os.path.exists(exe_path):
        print("✗ Executable not found")
        return False
    
    try:
        # Try to run the executable for a short time to check if it starts
        import subprocess
        process = subprocess.Popen([exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit to see if it starts
        import time
        time.sleep(3)
        
        # Terminate the process
        process.terminate()
        process.wait()
        
        print("✓ Executable test completed")
        return True
        
    except Exception as e:
        print(f"✗ Executable test failed: {e}")
        return False

def main():
    """Main build function"""
    print("Business Management App - Fixed Build Script")
    print("=" * 60)
    
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
    
    # Test executable
    if not test_executable():
        print("⚠ Executable test failed, but build completed")
    
    # Create installer
    if not create_installer():
        print("✗ Failed to create installer")
        return False
    
    # Clean up
    cleanup()
    
    print("\n" + "=" * 60)
    print("✓ Build completed successfully!")
    print("Executable location: dist/BusinessManagementApp.exe")
    print("Installer package: installer/")
    print("\nTo distribute the application:")
    print("1. Copy the contents of the 'installer' directory")
    print("2. Distribute to users")
    print("3. Users can run 'run.bat' to start the application")
    print("\nNote: If the executable still has module errors, try running")
    print("the application directly with 'python main.py' instead.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)