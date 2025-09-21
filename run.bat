@echo off
echo Business Management App
echo ========================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    echo Please install Python from https://python.org
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo Error: main.py not found
    echo Please make sure you are in the correct directory
    pause
    exit /b 1
)

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "database" mkdir database
if not exist "backup" mkdir backup
if not exist "resources" mkdir resources

echo Starting Business Management App...
echo.

REM Run the application
python main.py

pause