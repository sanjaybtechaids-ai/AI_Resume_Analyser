Write-Host "Starting AI Resume Analyser..." -ForegroundColor Cyan
Set-Location -Path $PSScriptRoot
streamlit run app.py
