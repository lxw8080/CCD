@echo off
setlocal enabledelayedexpansion

:: ============================================
:: CCD Project - No HMR Mode Startup Script (Windows)
:: ============================================

echo.
echo ========================================
echo   CCD Project - No HMR Mode
echo ========================================
echo.

:: Check if in project root directory
if not exist "backend" (
    echo ERROR: backend directory not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: frontend directory not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

:: ============================================
:: 1. Check backend dependencies
:: ============================================
echo [1/5] Checking backend dependencies...

if not exist "backend\venv" (
    echo ERROR: Python virtual environment not found
    echo Please create it first:
    echo   cd backend
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

if not exist "backend\venv\Scripts\python.exe" (
    echo ERROR: Virtual environment is incomplete
    echo Please recreate the virtual environment
    pause
    exit /b 1
)

echo Backend dependencies OK
echo.

:: ============================================
:: 2. Check frontend dependencies
:: ============================================
echo [2/5] Checking frontend dependencies...

if not exist "frontend\node_modules" (
    echo WARNING: node_modules not found
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    if errorlevel 1 (
        echo ERROR: Frontend dependency installation failed
        cd ..
        pause
        exit /b 1
    )
    cd ..
)

echo Frontend dependencies OK
echo.

:: ============================================
:: 3. Check port availability
:: ============================================
echo [3/5] Checking port availability...

netstat -ano | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo WARNING: Port 8000 is already in use
    echo Please stop the process or use stop-no-hmr.bat
    choice /C YN /M "Continue anyway (may fail)"
    if errorlevel 2 exit /b 1
)

netstat -ano | findstr ":3000" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo WARNING: Port 3000 is already in use
    echo Please stop the process or use stop-no-hmr.bat
    choice /C YN /M "Continue anyway (may fail)"
    if errorlevel 2 exit /b 1
)

echo Ports available
echo.

:: ============================================
:: 4. Start backend service
:: ============================================
echo [4/5] Starting backend service...

if not exist "logs" mkdir logs

start "CCD Backend (Django)" cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/auth/login/' -Method GET -TimeoutSec 5 -UseBasicParsing; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Backend may not have started correctly
    echo Please check the backend window for errors
    choice /C YN /M "Continue to start frontend"
    if errorlevel 2 exit /b 1
) else (
    echo Backend service started successfully (http://127.0.0.1:8000)
)
echo.

:: ============================================
:: 5. Build and start frontend service
:: ============================================
echo [5/5] Building and starting frontend service...

echo Building frontend project...
cd frontend
call npm run build
if errorlevel 1 (
    echo ERROR: Frontend build failed
    cd ..
    pause
    exit /b 1
)
cd ..

echo Frontend build complete
echo.

echo Starting frontend preview service...
start "CCD Frontend (Preview - No HMR)" cmd /k "cd frontend && npm run preview"

echo Waiting for frontend to start...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   Startup Complete!
echo ========================================
echo.
echo Backend Service: http://127.0.0.1:8000
echo Frontend Service: http://localhost:3000
echo.
echo Mode: Preview (Production Build)
echo - No HMR (Hot Module Replacement)
echo - No WebSocket connection
echo - Suitable for mobile testing (camera won't refresh page)
echo.
echo Notes:
echo - Code changes require rebuild
echo - Use stop-no-hmr.bat to stop services
echo - Logs saved in logs directory
echo.
echo Press any key to open in browser...
pause >nul

start http://localhost:3000

echo.
echo Services are running in background
echo Closing this window will not stop services
echo.

