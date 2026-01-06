#!/bin/bash

# AI-Compass Startup Script
# Starts both API and Streamlit in separate terminal windows

echo "🧭 AI-Compass Startup Script"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "apps/api" ] || [ ! -d "apps/web" ]; then
    echo -e "${YELLOW}⚠ Please run this script from the ai-compass root directory${NC}"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠ Virtual environment not detected.${NC}"
    echo "Activate it first with: source venv/bin/activate"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${BLUE}Starting AI-Compass components...${NC}"
echo ""

# Function to start API
start_api() {
    cd apps/api || exit
    echo -e "${GREEN}Starting FastAPI backend...${NC}"
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
}

# Function to start Streamlit
start_streamlit() {
    cd apps/web || exit
    echo -e "${GREEN}Starting Streamlit frontend...${NC}"
    streamlit run Home.py
}

# Check OS and start in appropriate way
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS"
    echo "Opening terminals for API and Streamlit..."
    
    # Start API in new terminal
    osascript -e 'tell application "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate 2>/dev/null; cd apps/api && uvicorn main:app --reload"' &
    
    # Wait a bit
    sleep 2
    
    # Start Streamlit in new terminal
    osascript -e 'tell application "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate 2>/dev/null; cd apps/web && streamlit run Home.py"' &
    
    echo -e "${GREEN}✓ Started in separate terminals${NC}"
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Detected Linux"
    
    # Try to detect terminal emulator
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd $(pwd) && source venv/bin/activate 2>/dev/null; cd apps/api && uvicorn main:app --reload; exec bash" &
        sleep 2
        gnome-terminal -- bash -c "cd $(pwd) && source venv/bin/activate 2>/dev/null; cd apps/web && streamlit run Home.py; exec bash" &
        echo -e "${GREEN}✓ Started in gnome-terminal${NC}"
    
    elif command -v konsole &> /dev/null; then
        konsole -e "cd $(pwd) && source venv/bin/activate 2>/dev/null; cd apps/api && uvicorn main:app --reload; bash" &
        sleep 2
        konsole -e "cd $(pwd) && source venv/bin/activate 2>/dev/null; cd apps/web && streamlit run Home.py; bash" &
        echo -e "${GREEN}✓ Started in konsole${NC}"
    
    else
        echo -e "${YELLOW}Could not detect terminal emulator. Starting in background...${NC}"
        cd apps/api && uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
        sleep 2
        cd "$(dirname "$0")" && cd apps/web && streamlit run Home.py &
    fi

else
    # Windows or other (tmux fallback)
    echo "Using tmux/screen for process management..."
    
    if command -v tmux &> /dev/null; then
        echo "Starting with tmux..."
        tmux new-session -d -s aicompass-api "cd apps/api && uvicorn main:app --reload"
        tmux new-session -d -s aicompass-web "cd apps/web && streamlit run Home.py"
        echo -e "${GREEN}✓ Started in tmux sessions${NC}"
        echo "  - Attach to API: tmux attach -t aicompass-api"
        echo "  - Attach to Web: tmux attach -t aicompass-web"
    else
        echo -e "${YELLOW}Manual start required:${NC}"
        echo ""
        echo "Terminal 1 (API):"
        echo "  cd apps/api && uvicorn main:app --reload"
        echo ""
        echo "Terminal 2 (Web):"
        echo "  cd apps/web && streamlit run Home.py"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}AI-Compass is starting up!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Access points (will be available shortly):"
echo "  📊 Streamlit UI:  http://localhost:8501"
echo "  🔌 API Server:    http://localhost:8000"
echo "  📖 API Docs:      http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop (if running in foreground)"
echo ""

# Wait for user input if running in foreground
if [[ "$1" != "--background" ]]; then
    read -p "Press Enter to exit this script (services will keep running)..." 
fi
