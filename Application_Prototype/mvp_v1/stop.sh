#!/bin/bash

echo "Stopping AI-Compass Processes..."

# Find pids for uvicorn and vite/node related to this project might be tricky
# A simple killall approach or pkill for user owned processes
# For dev environment:

# Check appropriate kill command for OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash)
    echo "Detected Windows. Using taskkill..."
    # Killing python/node globally in this shell's context is the most reliable way 
    # for a dev script without PID tracking.
    taskkill //F //IM python.exe //T 2> /dev/null || echo "No Python processes found."
    taskkill //F //IM node.exe //T 2> /dev/null || echo "No Node processes found."
else
    # Mac/Linux
    pkill -f "uvicorn main:app" || echo "Backend not running."
    pkill -f "vite" || echo "Frontend not running."
fi

echo "Done."
