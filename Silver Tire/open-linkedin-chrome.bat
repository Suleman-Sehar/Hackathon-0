@echo off
echo Opening LinkedIn in Google Chrome...
echo.

REM Find Chrome installation
set "CHROME_PATH="
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set "CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set "CHROME_PATH=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
)

if "%CHROME_PATH%"=="" (
    echo ERROR: Google Chrome not found!
    echo Please install Chrome from: https://www.google.com/chrome/
    pause
    exit /b 1
)

echo Found Chrome: %CHROME_PATH%
echo.
echo Opening LinkedIn login in Chrome...
start "" "%CHROME_PATH%" "https://www.linkedin.com/login"
echo.
echo Chrome should now be opening with LinkedIn login.
echo.
echo NEXT STEPS:
echo 1. Login to LinkedIn in Chrome
echo 2. Navigate to your feed
echo 3. Stay for 10 seconds
echo 4. Keep Chrome open
echo 5. Go back to dashboard and click "Test LinkedIn Post"
echo.
pause
