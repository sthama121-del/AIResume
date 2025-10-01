#!/bin/bash

# AIResume Run Script
# Quick script to activate environment and run the app

echo "🚀 Starting AIResume..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first:"
    echo "  chmod +x setup.sh"
    echo "  ./setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Please run setup.sh first"
    exit 1
fi

# Run the application
echo "✅ Starting Streamlit application..."
echo "🌐 Opening browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
