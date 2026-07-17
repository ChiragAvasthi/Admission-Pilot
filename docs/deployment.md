# AdmissionPilot - Deployment Guide

## Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for native frontend dev)
- Python 3.11+ (for native backend dev)
- Ollama (running natively on the host machine)

## 1. Native Local Deployment (Recommended for Development)

We provide PowerShell helper scripts to make native deployment trivial.

### Initial Setup
1. Duplicate `.env.development` to `.env` in the root folder.
2. Ensure Ollama is running natively on your machine and has the `qwen3:8b` model pulled (`ollama run qwen3:8b`).

### Starting the Stack
Run the start script from the `scripts/` directory:
```powershell
cd scripts
.\start.ps1
```
This script will:
- Set up the `.env` file.
- Launch the FastAPI backend in a new window (`http://localhost:8000`).
- Launch the React frontend in a new window (`http://localhost:5173`).

### Backups and Restores
To backup the SQLite database and workspaces:
```powershell
cd scripts
.\backup.ps1
```
To restore:
```powershell
cd scripts
.\restore.ps1 -BackupZip "..\backups\20231010_120000.zip"
```

## 2. Docker Deployment (Recommended for Production/Testing)

The provided `docker-compose.yml` configures a multi-stage optimized build for both the frontend (Nginx) and backend.

### Setup
1. Duplicate `.env.production` to `.env` in the root folder.
2. Edit `.env` and change `SECRET_KEY` to a secure random string.
3. Edit `CORS_ORIGINS` to match your frontend domain.

### Running Docker Compose
```bash
docker-compose up -d --build
```

### Important Docker Notes
- **Ollama Connectivity**: The `docker-compose.yml` uses `host.docker.internal` to allow the containerized backend to communicate with Ollama running natively on your host machine.
- **Data Persistence**: The SQLite database and ChromaDB vectors are stored in the `backend_data` volume and the `./company_workspaces` directory.
