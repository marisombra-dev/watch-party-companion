#!/bin/bash

# Watch Party Nova - Easy Setup Script

echo "=================================="
echo "   Watch Party Nova Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed."
    echo "   Please install from: https://ollama.ai"
    echo "   Then run this script again."
    exit 1
fi

echo "✓ Ollama found"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Some packages failed to install."
    echo "   If pyaudio failed, try:"
    echo ""
    echo "   On macOS:"
    echo "     brew install portaudio"
    echo "     pip install pyaudio"
    echo ""
    echo "   On Linux:"
    echo "     sudo apt-get install portaudio19-dev python3-pyaudio"
    echo "     pip install pyaudio"
    echo ""
fi

# Pull LLaVA model
echo ""
echo "🤖 Downloading LLaVA model (this may take a few minutes)..."
ollama pull llava:7b

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Failed to download LLaVA model."
    echo "   Make sure Ollama is running:"
    echo "     ollama serve"
    exit 1
fi

echo ""
echo "=================================="
echo "   ✅ Setup Complete!"
echo "=================================="
echo ""
echo "To run Watch Party Nova:"
echo "  python watchparty_voice_final.py"
echo ""
echo "Enjoy watching with Nova! 🐿️🎬"
