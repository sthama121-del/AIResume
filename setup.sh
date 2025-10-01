#!/bin/bash

# AIResume Setup Script for macOS/Linux
# This script automates the setup process

echo "🚀 AIResume Setup Script"
echo "========================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the AIResume directory"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi

# Verify .env file
echo ""
echo "🔑 Checking API key configuration..."
if [ -f ".env" ]; then
    if grep -q "OPENROUTER_API_KEY" .env; then
        echo "✅ OpenRouter API key found"
    else
        echo "⚠️  Warning: OPENROUTER_API_KEY not found in .env"
        echo "Please add your OpenRouter API key to .env file"
    fi
else
    echo "❌ Error: .env file not found"
    echo "Please create .env file with: OPENROUTER_API_KEY=your_key_here"
    exit 1
fi

# Create uploads directory if it doesn't exist
mkdir -p uploads

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 AIResume is ready to use!"
echo ""
echo "To start the application, run:"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
echo "Or simply run:"
echo "  ./run.sh"
echo ""
