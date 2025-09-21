@echo off
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
