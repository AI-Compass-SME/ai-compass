#!/bin/bash
set -e

echo "=========================================="
echo "Setting up AI-Compass Prototype Environment (Mac/Linux)"
echo "=========================================="

# get base dir and root dir
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$(dirname "$BASE_DIR")")" # Go up 2 levels -> Application_Prototype -> root? Verify path depth.
# BASE_DIR is .../Application_Prototype/mvp_v1
# dirname(BASE_DIR) -> .../Application_Prototype
# dirname(...) -> .../Projects/ai-compass (ROOT)
ROOT_DIR="$BASE_DIR/../.."

cd "$BASE_DIR"

echo "[1/2] Verifying Root Virtual Environment..."
if [ ! -d "$ROOT_DIR/.venv" ]; then
    echo "Error: Root virtual environment not found at $ROOT_DIR/.venv"
    echo "Please ensure the project root has the virtual environment set up."
    exit 1
fi

echo "Installing Python dependencies into ROOT .venv..."
if [ -d "$ROOT_DIR/.venv/Scripts" ]; then
    source "$ROOT_DIR/.venv/Scripts/activate"
else
    source "$ROOT_DIR/.venv/bin/activate"
fi
cd backend
pip install -r requirements.txt
cd "$BASE_DIR"

echo ""
echo "[2/2] Setting up Frontend..."
if [ ! -d "frontend" ]; then
    echo "Error: Frontend directory not found."
    exit 1
fi

cd frontend
echo "Installing npm dependencies..."
npm install
cd "$BASE_DIR"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "Use ./start.sh to run the application."
echo "=========================================="
