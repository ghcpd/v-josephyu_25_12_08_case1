#!/bin/bash
# Setup script for Linux/Mac
# Creates virtual environment and installs dependencies

set -e  # Exit on any error

echo "Flask Login App - Setup Script (Bash)"
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Create virtual environment
echo "Creating virtual environment (.venv)..."
python3 -m venv .venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Initialize database
echo "Initializing database..."
python3 -c "from app import app; from models import init_db; app.app_context().push(); init_db(app)"
echo "✓ Database initialized"
echo ""

echo "======================================"
echo "Setup completed successfully!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To start the app, run:"
echo "  python3 app.py"
echo ""
echo "To run tests, run:"
echo "  ./run_tests.sh"
echo ""
