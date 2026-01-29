#!/bin/bash

echo "=========================================="
echo "Starting AI-Compass Prototype (Mac/Linux)"
echo "=========================================="

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$BASE_DIR/../.."
cd "$BASE_DIR"

# Check if root venv exists
if [ ! -d "$ROOT_DIR/.venv" ]; then
    echo "Error: Root virtual environment not found at $ROOT_DIR/.venv"
    exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "Error: node_modules not found. Please run ./setup.sh first."
    exit 1
fi

# Function to kill background processes on exit
cleanup() {
    echo ""
    echo "Stopping processes..."
    # Kill the process groups
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

echo "Launching Backend (FastAPI)..."
cd backend
if [ -d "$ROOT_DIR/.venv/Scripts" ]; then
    source "$ROOT_DIR/.venv/Scripts/activate"
else
    source "$ROOT_DIR/.venv/bin/activate"
fi
# Point to root .env explicitely
uvicorn main:app --reload --port 8000 --env-file "$ROOT_DIR/.env" &
cd "$BASE_DIR"

echo "Launching Frontend (Vite)..."
cd frontend
npm run dev &
cd "$BASE_DIR"

echo ""
echo "=========================================="
echo "Application is starting!"
echo "Backend API Docs: http://localhost:8000/docs"
echo "Frontend URL:      http://localhost:5173"
echo "=========================================="
echo "Press Ctrl+C to stop both servers."

# Wait for background processes
wait
