param (
    [string]$Env = "development"
)

Write-Host "Starting AdmissionPilot in $Env environment..." -ForegroundColor Cyan

# Set environment
Copy-Item -Path "..\.env.$Env" -Destination "..\.env" -Force

# Check for Docker option
if ($args -contains "--docker") {
    Write-Host "Starting via Docker Compose..." -ForegroundColor Yellow
    cd ..
    docker-compose up -d --build
} else {
    Write-Host "Starting natively..." -ForegroundColor Yellow
    
    # Start Backend
    Write-Host "Starting FastAPI Backend..."
    Start-Process -FilePath "powershell.ps1" -ArgumentList "-NoExit -Command `"cd ..\backend; .\venv\Scripts\activate; uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`"" -WindowStyle Normal

    # Start Frontend
    Write-Host "Starting React Frontend..."
    Start-Process -FilePath "powershell.ps1" -ArgumentList "-NoExit -Command `"cd ..\frontend; npm run dev`"" -WindowStyle Normal

    Write-Host "Stack is starting up in separate windows!" -ForegroundColor Green
}
