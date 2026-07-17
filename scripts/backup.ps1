$BackupDir = "..\backups\$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null

Write-Host "Starting Backup to $BackupDir..." -ForegroundColor Cyan

# 1. Backup SQLite Database
if (Test-Path "..\backend\admission_pilot.db") {
    Copy-Item "..\backend\admission_pilot.db" -Destination "$BackupDir\admission_pilot.db"
    Write-Host "Backed up Database." -ForegroundColor Green
}

# 2. Backup Uploads / ChromaDB
if (Test-Path "..\backend\company_workspaces") {
    Copy-Item -Recurse "..\backend\company_workspaces" -Destination "$BackupDir\company_workspaces"
    Write-Host "Backed up Workspaces & ChromaDB." -ForegroundColor Green
}

# 3. Zip the backup
Compress-Archive -Path "$BackupDir\*" -DestinationPath "$BackupDir.zip" -Force
Remove-Item -Recurse -Force $BackupDir

Write-Host "Backup completed successfully: $BackupDir.zip" -ForegroundColor Green
