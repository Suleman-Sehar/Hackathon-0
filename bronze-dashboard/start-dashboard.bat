@echo off
echo.
echo ======================================================================
echo   BRONZE TIRE DASHBOARD - Next.js
echo   Sophisticated Modern UI for AI Employee Operations
echo ======================================================================
echo.
echo Starting development server...
echo.
echo Dashboard will open at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.
echo ======================================================================
echo.

cd /d "%~dp0"

if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    echo.
)

call npm run dev

pause
