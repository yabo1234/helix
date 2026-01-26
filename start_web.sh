#!/bin/bash
# Quick start script for Triple Helix Innovation Chatbot Web Interface

echo "============================================================"
echo "Triple Helix Innovation Chatbot - Quick Start"
echo "============================================================"
echo ""

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY environment variable is not set"
    echo ""
    echo "To use the chatbot, you need to set your OpenAI API key:"
    echo "  export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "Get your API key from: https://platform.openai.com/api-keys"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Check if dependencies are installed
echo "Checking dependencies..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip install -q -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✓ Dependencies installed successfully"
    else
        echo "✗ Failed to install dependencies"
        echo "Please run: pip install -r requirements.txt"
        exit 1
    fi
else
    echo "✓ Dependencies already installed"
fi

echo ""
echo "============================================================"
echo "Starting Web Interface..."
echo "============================================================"
echo ""
echo "📱 Open your browser and navigate to:"
echo "   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "============================================================"
echo ""

# Start the web interface
python3 web_interface.py
