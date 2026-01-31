# PowerShell setup script
python -m venv .venv
. \.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Write-Host "Virtual environment created and dependencies installed. Activate with: . \.venv\Scripts\Activate.ps1"