#!/bin/bash
# Installation script for Arch Linux AI CLI

set -e

echo "🐧 Arch Linux AI CLI Installer"
echo "=============================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Error: This tool is designed for Linux systems"
    exit 1
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Install it with: sudo pacman -S python"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.7"

if [[ $(echo -e "$PYTHON_VERSION\n$REQUIRED_VERSION" | sort -V | head -n1) != "$REQUIRED_VERSION" ]]; then
    echo "❌ Error: Python 3.7 or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip is not installed"
    echo "Install it with: sudo pacman -S python-pip"
    exit 1
fi

echo "✓ pip detected"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt --user

echo "✓ Dependencies installed"
echo ""

# Make script executable
chmod +x archlinux-ai-cli.py

echo "✓ Script made executable"
echo ""

# Ask user where to install
echo "Where would you like to install archlinux-ai-cli?"
echo "1) System-wide (/usr/local/bin) - requires sudo"
echo "2) User directory (~/.local/bin)"
echo "3) Don't install, just keep in current directory"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "Installing system-wide..."
        sudo cp archlinux-ai-cli.py /usr/local/bin/archlinux-ai-cli
        echo "✓ Installed to /usr/local/bin/archlinux-ai-cli"
        ;;
    2)
        echo ""
        echo "Installing to user directory..."
        mkdir -p ~/.local/bin
        cp archlinux-ai-cli.py ~/.local/bin/archlinux-ai-cli
        echo "✓ Installed to ~/.local/bin/archlinux-ai-cli"
        echo ""
        echo "⚠️  Make sure ~/.local/bin is in your PATH"
        if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
            echo "Add this to your ~/.bashrc or ~/.zshrc:"
            echo 'export PATH="$HOME/.local/bin:$PATH"'
        fi
        ;;
    3)
        echo ""
        echo "Skipping installation. You can run it with:"
        echo "./archlinux-ai-cli.py"
        ;;
    *)
        echo "Invalid choice. Skipping installation."
        ;;
esac

echo ""
echo "=============================="
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Get your free API key from: https://makersuite.google.com/app/apikey"
echo "2. Set your API key:"
echo "   export GOOGLE_AI_API_KEY='your-api-key-here'"
echo "   Or: echo 'your-api-key' > ~/.config/archlinux-ai-cli/api_key"
echo ""
echo "3. Try it out:"
echo "   archlinux-ai-cli -q 'How do I update my system?'"
echo "   archlinux-ai-cli -i  # Interactive mode"
echo ""
echo "For help: archlinux-ai-cli --help"
echo ""
echo "Stay rolling! 🚀"
