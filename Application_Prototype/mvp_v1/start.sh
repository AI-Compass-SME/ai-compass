#!/bin/bash
echo "Starting AI Compass MVP v1..."

# Function to handle cleanup on exit
cleanup() {
    echo "Stopping services..."
    kill $(jobs -p)
    exit
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo "Starting Backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "Starting Frontend..."
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Application started!"
echo "Frontend: http://localhost:5173"
echo "Backend: http://localhost:8000/docs"

wait $BACKEND_PID $FRONTEND_PID
