@echo off
setlocal enabledelayedexpansion

:: ============================================
:: CCD Project Stop Script (Windows)
:: ============================================

echo.
echo ========================================
echo   CCD Project - Stop Services
echo ========================================
echo.

:: Stop backend service (port 8000)
echo [1/4] Stopping backend service (port 8000)...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo Found process PID: %%a
    taskkill /F /PID %%a >nul 2>&1
    if !errorlevel! equ 0 (
        echo Backend service stopped successfully
    )
)

echo.

:: Stop frontend service (port 3000)
echo [2/4] Stopping frontend service (port 3000)...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000" ^| findstr "LISTENING"') do (
    echo Found process PID: %%a
    taskkill /F /PID %%a >nul 2>&1
    if !errorlevel! equ 0 (
        echo Frontend service stopped successfully
    )
)

echo.

:: Close related windows
echo [3/4] Closing related windows...

taskkill /FI "WINDOWTITLE eq CCD Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq CCD Frontend*" /F >nul 2>&1

echo Related windows closed
echo.

:: Verify services stopped
echo [4/4] Verifying service status...

netstat -ano | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if errorlevel 1 (
    echo Backend service stopped completely
) else (
    echo WARNING: Backend service still running on port 8000
)

netstat -ano | findstr ":3000" | findstr "LISTENING" >nul 2>&1
if errorlevel 1 (
    echo Frontend service stopped completely
) else (
    echo WARNING: Frontend service still running on port 3000
)

echo.
echo ========================================
echo   Stop Complete!
echo ========================================
echo.

if exist "logs\backend.log" (
    echo Log files saved in logs directory
)

echo.
pause

