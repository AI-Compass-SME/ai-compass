@echo off
echo Starting AI Compass MVP v1...

:: Start Backend
start "AI Compass Backend" cmd /k "cd backend && venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload --port 8000"

:: Start Frontend
start "AI Compass Frontend" cmd /k "cd frontend && npm install && npm run dev"

echo Application started!
echo Frontend: http://localhost:5173
echo Backend: http://localhost:8000/docs
pause
