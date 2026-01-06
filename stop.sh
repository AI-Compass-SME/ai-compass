#!/bin/bash

# ==============================================================================
# AI-Compass Stop Script
# ==============================================================================
# Stops both FastAPI backend and Streamlit frontend
# Works on macOS, Linux, and WSL
# ==============================================================================

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}║              🛑 AI-Compass Stop Script                     ║${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ==============================================================================
# Helper Functions
# ==============================================================================

print_step() {
    echo -e "${GREEN}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# ==============================================================================
# Stop FastAPI (Uvicorn)
# ==============================================================================

print_step "Stopping FastAPI backend..."

if command -v pgrep &> /dev/null; then
    # Using pgrep (more reliable)
    UVICORN_PIDS=$(pgrep -f "uvicorn.*main:app")
    
    if [ -n "$UVICORN_PIDS" ]; then
        echo "Found uvicorn processes: $UVICORN_PIDS"
        kill $UVICORN_PIDS 2>/dev/null
        sleep 1
        
        # Force kill if still running
        REMAINING=$(pgrep -f "uvicorn.*main:app")
        if [ -n "$REMAINING" ]; then
            print_warning "Force killing stubborn uvicorn processes..."
            kill -9 $REMAINING 2>/dev/null
        fi
        
        print_success "FastAPI backend stopped"
    else
        print_warning "No uvicorn processes found"
    fi
else
    # Fallback: using pkill
    if pkill -f "uvicorn.*main:app" 2>/dev/null; then
        sleep 1
        pkill -9 -f "uvicorn.*main:app" 2>/dev/null  # Force kill if needed
        print_success "FastAPI backend stopped"
    else
        print_warning "No uvicorn processes found"
    fi
fi

# ==============================================================================
# Stop Streamlit
# ==============================================================================

print_step "Stopping Streamlit frontend..."

if command -v pgrep &> /dev/null; then
    # Using pgrep
    STREAMLIT_PIDS=$(pgrep -f "streamlit.*run")
    
    if [ -n "$STREAMLIT_PIDS" ]; then
        echo "Found streamlit processes: $STREAMLIT_PIDS"
        kill $STREAMLIT_PIDS 2>/dev/null
        sleep 1
        
        # Force kill if still running
        REMAINING=$(pgrep -f "streamlit.*run")
        if [ -n "$REMAINING" ]; then
            print_warning "Force killing stubborn streamlit processes..."
            kill -9 $REMAINING 2>/dev/null
        fi
        
        print_success "Streamlit frontend stopped"
    else
        print_warning "No streamlit processes found"
    fi
else
    # Fallback: using pkill
    if pkill -f "streamlit.*run" 2>/dev/null; then
        sleep 1
        pkill -9 -f "streamlit.*run" 2>/dev/null  # Force kill if needed
        print_success "Streamlit frontend stopped"
    else
        print_warning "No streamlit processes found"
    fi
fi

# ==============================================================================
# Additional cleanup for port-based killing
# ==============================================================================

print_step "Checking ports 8000 and 8501..."

# Function to kill process on specific port
kill_port() {
    local port=$1
    local name=$2
    
    if command -v lsof &> /dev/null; then
        PID=$(lsof -ti:$port 2>/dev/null)
        if [ -n "$PID" ]; then
            print_warning "Found process on port $port (PID: $PID), killing..."
            kill $PID 2>/dev/null
            sleep 1
            kill -9 $PID 2>/dev/null  # Force kill if needed
            print_success "Process on port $port stopped"
        fi
    elif command -v netstat &> /dev/null; then
        # Windows/WSL fallback
        if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
            # Windows PowerShell command
            echo "Checking port $port on Windows..."
        else
            # Linux netstat
            PID=$(netstat -ltnp 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d'/' -f1)
            if [ -n "$PID" ]; then
                print_warning "Found process on port $port (PID: $PID), killing..."
                kill $PID 2>/dev/null
                sleep 1
                kill -9 $PID 2>/dev/null
                print_success "Process on port $port stopped"
            fi
        fi
    fi
}

# Kill processes on specific ports
kill_port 8000 "API"
kill_port 8501 "Streamlit"

# ==============================================================================
# Verification
# ==============================================================================

echo ""
print_step "Verifying shutdown..."
echo ""

REMAINING_UVICORN=$(pgrep -f "uvicorn.*main:app" 2>/dev/null || echo "")
REMAINING_STREAMLIT=$(pgrep -f "streamlit.*run" 2>/dev/null || echo "")

if [ -z "$REMAINING_UVICORN" ] && [ -z "$REMAINING_STREAMLIT" ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}║           ✓ All services stopped successfully! 🛑          ║${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Both FastAPI and Streamlit have been stopped."
    echo "Ports 8000 and 8501 are now free."
    echo ""
else
    print_warning "Some processes may still be running:"
    if [ -n "$REMAINING_UVICORN" ]; then
        echo "  Uvicorn: PIDs $REMAINING_UVICORN"
    fi
    if [ -n "$REMAINING_STREAMLIT" ]; then
        echo "  Streamlit: PIDs $REMAINING_STREAMLIT"
    fi
    echo ""
    echo "Try running this script again or manually kill with:"
    echo "  pkill -9 -f uvicorn"
    echo "  pkill -9 -f streamlit"
fi

echo ""
echo -e "${BLUE}To start again, run:${NC}"
echo "  bash start.sh"
echo ""
