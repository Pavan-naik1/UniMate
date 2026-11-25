@echo off
title UniMate Launcher
cd /d "%~dp0"

if exist "%LOCALAPPDATA%\Programs\nodejs" (
    set "PATH=%LOCALAPPDATA%\Programs\nodejs;%PATH%"
)

echo ==========================================
echo       UniMate AI University Assistant
echo ==========================================
echo.

echo Checking Python...
python --version
if errorlevel 1 goto ERROR

echo Checking Node.js...
node --version
if errorlevel 1 goto ERROR

echo.
echo Starting backend...
if not exist "venv\Scripts\python.exe" goto NOVENV

start "UniMate Backend" cmd /k "venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000"

echo.
echo Starting frontend...
if not exist "frontend\node_modules" goto NONPM

start "UniMate Frontend" /D "%~dp0frontend" cmd /k "npm run dev -- --host 127.0.0.1"

echo.
echo Waiting for application...
timeout /t 8 /nobreak

echo.
echo Opening UniMate in browser...
start http://127.0.0.1:5173

echo.
echo If the browser does not open, check the two terminal windows.
pause
exit /b

:NOVENV
echo ERROR: Python virtual environment not found.
echo Please share the project folder structure.
pause
exit /b 1

:NONPM
echo ERROR: Frontend node_modules folder not found.
echo Please run npm install inside the frontend folder.
pause
exit /b 1

:ERROR
echo ERROR: Python or Node.js is not available.
pause
exit /b 1