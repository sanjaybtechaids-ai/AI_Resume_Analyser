Write-Host "Starting ResumeIQ..." -ForegroundColor Cyan
Set-Location -Path $PSScriptRoot
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
