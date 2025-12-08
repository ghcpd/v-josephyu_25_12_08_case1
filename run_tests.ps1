# Test runner script for Windows PowerShell
# Runs pytest with proper configuration

Write-Host "Flask Login App - Test Suite (PowerShell)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment if not already activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\.venv\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
}

Write-Host ""
Write-Host "Python version:" -ForegroundColor Cyan
python --version
Write-Host ""

# Run tests
Write-Host "Running test suite (test_app.py)..." -ForegroundColor Yellow
Write-Host ""

python -m pytest test_app.py -v --tb=short

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Test run completed!" -ForegroundColor Green
Write-Host ""
