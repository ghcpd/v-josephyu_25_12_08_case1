# Setup script for Windows PowerShell
# Creates virtual environment and installs dependencies

Write-Host "Flask Login App - Setup Script (PowerShell)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python version:" -ForegroundColor Green
    Write-Host $pythonVersion
    Write-Host ""
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Yellow
python -m venv .venv
Write-Host "✓ Virtual environment created" -ForegroundColor Green
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null
Write-Host "✓ pip upgraded" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt | Out-Null
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python -c "from app import app; from models import init_db; app.app_context().push(); init_db(app)" 2>&1 | Out-Null
Write-Host "✓ Database initialized" -ForegroundColor Green
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the app, run:" -ForegroundColor Cyan
Write-Host "  python app.py" -ForegroundColor White
Write-Host ""
Write-Host "To run tests, run:" -ForegroundColor Cyan
Write-Host "  .\run_tests.ps1" -ForegroundColor White
Write-Host ""
