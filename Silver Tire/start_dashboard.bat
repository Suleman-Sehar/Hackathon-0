@echo off
echo ============================================================
echo   Silver Tier Dashboard Launcher
echo   AI Employee v0.2 - Autonomous Automation
echo ============================================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

echo Starting Dashboard Server...
echo Dashboard will open at: http://localhost:8001
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python launch_dashboard.py

pause
