#!/usr/bin/env pwsh
# PowerShell setup script — create venv and install requirements
python -m venv .venv
Write-Output "Activating virtual environment (PowerShell)"
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
