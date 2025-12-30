# Ada v2 Auto-Fix Script
# Double-click this file to automatically apply all bug fixes

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Ada v2 Automatic Bug Fix Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Get the directory where this script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Change to the backend directory
Set-Location $scriptDir

Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python or ensure it's in your PATH" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "Running fix script..." -ForegroundColor Yellow
Write-Host ""

# Run the Python fix script
python fix_bugs.py

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Press any key to exit..." -ForegroundColor Cyan
pause
