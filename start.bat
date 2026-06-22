@echo off
setlocal enabledelayedexpansion

REM Get port from command line argument, default to 8089 if not provided
set PORT=%1
if "%PORT%"=="" set PORT=8089

REM Set the ngrok URL
set NGROK_URL=30e1b7c2cc18-7054659292749497477.ngrok-free.app

REM Check if ngrok is already running
tasklist /FI "IMAGENAME eq ngrok.exe" 2>NUL | find /I /N "ngrok.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo.
    echo ERROR: Ngrok is already running!
    echo Please stop the existing ngrok process first.
    echo.
    pause
    exit /b 1
)

REM Print the URL
echo.
echo ========================================
echo Ngrok URL: https://%NGROK_URL%
echo Port: %PORT%
echo ========================================
echo.
echo Starting ngrok... Press Ctrl+C to stop.
echo.

REM Run ngrok (this will run continuously until stopped)
REM Use --domain flag for ngrok v3+ (correct syntax: ngrok http PORT --domain=DOMAIN)
ngrok http %PORT% --domain=%NGROK_URL%

