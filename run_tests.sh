#!/bin/bash
# Test runner script for Linux/Mac
# Runs pytest with proper configuration

set -e  # Exit on any error

echo "Flask Login App - Test Suite (Bash)"
echo "===================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment not activated. Activating..."
    source .venv/bin/activate
fi

echo "Python version:"
python3 --version
echo ""

# Run tests
echo "Running test suite (test_app.py)..."
echo ""

python3 -m pytest test_app.py -v --tb=short

echo ""
echo "===================================="
echo "Test run completed!"
echo ""
