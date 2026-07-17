$Confirm = Read-Host "WARNING: This will delete the database and all uploaded files. Are you sure? (Y/N)"
if ($Confirm -ne 'Y') {
    Write-Host "Reset cancelled."
    exit 0
}

Write-Host "Resetting environment..." -ForegroundColor Yellow

if (Test-Path "..\backend\admission_pilot.db") {
    Remove-Item -Force "..\backend\admission_pilot.db"
    Write-Host "Database deleted."
}

if (Test-Path "..\backend\company_workspaces") {
    Remove-Item -Recurse -Force "..\backend\company_workspaces"
    Write-Host "Workspaces deleted."
}

if (Test-Path "..\backend\logs") {
    Remove-Item -Recurse -Force "..\backend\logs"
    Write-Host "Logs deleted."
}

Write-Host "Applying fresh migrations..."
cd ..\backend
.\venv\Scripts\alembic upgrade head

Write-Host "Environment reset complete!" -ForegroundColor Green
