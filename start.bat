@echo off
REM AI-Compass Startup Script for Windows
REM Starts both API and Streamlit in separate windows

echo.
echo ==========================================
echo    AI-Compass Startup Script (Windows)
echo ==========================================
echo.

REM Check if we're in the right directory
if not exist "README.md" (
    echo ERROR: Please run this script from the ai-compass root directory
    pause
    exit /b 1
)

if not exist "apps\api" (
    echo ERROR: apps\api directory not found
    pause
    exit /b 1
)

if not exist "apps\web" (
    echo ERROR: apps\web directory not found
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo WARNING: Virtual environment not found at venv\Scripts\activate.bat
    echo.
    echo Please create it first with:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo Starting AI-Compass components...
echo.

REM Start API in new window
echo Starting FastAPI backend...
start "AI-Compass API" cmd /k "cd /d %~dp0apps\api && ..\..\venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for API to start
timeout /t 3 /nobreak >nul

REM Start Streamlit in new window
echo Starting Streamlit frontend...
start "AI-Compass Web" cmd /k "cd /d %~dp0apps\web && ..\..\venv\Scripts\activate && streamlit run Home.py"

echo.
echo ================================
echo   AI-Compass is starting up!
echo ================================
echo.
echo Access points (will be available shortly):
echo   - Streamlit UI:  http://localhost:8501
echo   - API Server:    http://localhost:8000
echo   - API Docs:      http://localhost:8000/docs
echo.
echo Two new windows have opened:
echo   1. "AI-Compass API" - FastAPI backend
echo   2. "AI-Compass Web" - Streamlit frontend
echo.
echo Close those windows to stop the services.
echo.
pause
