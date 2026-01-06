#!/bin/bash

# AI-Compass Streamlit App Runner
# This script runs the Streamlit multipage application

cd "$(dirname "$0")"

echo "🧭 Starting AI-Compass Streamlit Application..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit is not installed."
    echo "Installing dependencies from requirements.txt..."
    
    # Try pip3 first, then pip
    if command -v pip3 &> /dev/null; then
        pip3 install -r ../../requirements.txt
    elif command -v pip &> /dev/null; then
        pip install -r ../../requirements.txt
    else
        echo "❌ Error: pip is not installed. Please install pip first."
        exit 1
    fi
fi

# Run Streamlit
echo ""
echo "✅ Starting Streamlit server..."
echo "📍 Navigate to http://localhost:8501 in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run Home.py --server.port=8501 --server.address=localhost
