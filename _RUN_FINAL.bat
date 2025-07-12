@echo off
echo ========================================
echo    Albion Radar Python - Launcher
echo ========================================
echo.

echo Starting Albion Radar Web Interface...
echo.
echo Web Interface: http://localhost:5000
echo Radar Data:    http://localhost:5000/api/radar-data
echo Settings:      http://localhost:5000/settings
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
python -m albion_radar.web_interface

pause 