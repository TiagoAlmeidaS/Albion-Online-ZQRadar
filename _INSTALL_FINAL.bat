@echo off
echo ========================================
echo    Albion Radar Python - Installer
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo [2/4] Installing required packages...
pip install flask flask-socketio scapy psutil

echo.
echo [3/4] Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "config" mkdir config

echo.
echo [4/4] Setting up configuration files...
echo {} > radar_settings.json
echo {"players": [], "guilds": []} > ignore_list.json

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo To start the radar:
echo   1. Run _RUN.bat
echo   2. Open http://localhost:5000 in your browser
echo   3. Configure settings and start the radar
echo.
echo For help, see README.md
echo.
pause 