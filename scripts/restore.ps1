param(
    [Parameter(Mandatory=$true)][string]$BackupZip
)

if (-Not (Test-Path $BackupZip)) {
    Write-Host "Backup file not found!" -ForegroundColor Red
    exit 1
}

$Confirm = Read-Host "Are you sure you want to restore from $BackupZip? This will overwrite current data! (Y/N)"
if ($Confirm -ne 'Y') {
    Write-Host "Restore cancelled."
    exit 0
}

Write-Host "Restoring from $BackupZip..." -ForegroundColor Cyan

$TempDir = "..\backups\temp_restore"
Expand-Archive -Path $BackupZip -DestinationPath $TempDir -Force

# 1. Restore Database
if (Test-Path "$TempDir\admission_pilot.db") {
    Copy-Item "$TempDir\admission_pilot.db" -Destination "..\backend\admission_pilot.db" -Force
}

# 2. Restore Workspaces
if (Test-Path "$TempDir\company_workspaces") {
    Copy-Item -Recurse -Force "$TempDir\company_workspaces\*" -Destination "..\backend\company_workspaces"
}

Remove-Item -Recurse -Force $TempDir

Write-Host "Restore completed successfully." -ForegroundColor Green
