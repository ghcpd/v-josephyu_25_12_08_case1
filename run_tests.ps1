#!/usr/bin/env pwsh
Write-Output "Running pytest (PowerShell)"
& ".\.venv\Scripts\python.exe" -m pytest -q test_files
