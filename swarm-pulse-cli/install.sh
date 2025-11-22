#!/bin/bash
# Swarm Pulse CLI - One-Command Install

echo "🌊 Swarm Pulse CLI - Installing..."
echo ""

# Install Python if needed
if ! command -v python3 &> /dev/null; then
    echo "📦 Installing Python..."
    sudo apt update && sudo apt install -y python3 python3-pip
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -q rich

# Make executable
chmod +x monitor.py

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 Run with:"
echo "   ./monitor.py"
echo ""
echo "   or"
echo ""
echo "   python3 monitor.py"
echo ""
