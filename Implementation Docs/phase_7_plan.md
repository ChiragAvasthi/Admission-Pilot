# AdmissionPilot - Phase 7: Production-Ready Local Deployment Implementation Plan

## Final Decisions
- **Scripting Environment**: Standard PowerShell (`.ps1`) scripts will be created for helper commands.
- **Security/Rate Limiting**: `slowapi` will be implemented.
- **Docker/Ollama**: Ollama will be assumed to run natively on the host machine (`host.docker.internal`) to simplify local GPU utilization.

## Proposed Changes

### 1. Docker & Containerization
- **Backend**: Create an optimized multi-stage `backend/Dockerfile`.
- **Frontend**: Create an optimized multi-stage `frontend/Dockerfile` using Nginx for production serving.
- **Root**: Refactor `docker-compose.yml` to define the frontend, backend, database persistence, and ChromaDB volumes.

### 2. Environment Management
- **Action**: Create `.env.development`, `.env.testing`, and `.env.production` templates.

### 3. Security, Logging, and Monitoring
- **Action**: Update `backend/app/main.py` to include strict CORS, `slowapi` rate limiting, and size limit middleware.
- **Action**: Implement structured JSON logging using the `logging` library for app logs, access logs, and error logs with rotation mechanisms.

### 4. Health Checks
- **Action**: Create `backend/app/api/v1/endpoints/health.py` containing `/health/live` (basic ping), `/health/ready` (DB & ChromaDB connection checks), and standard `/health`.

### 5. Backup & Restore Scripts
- **Action**: Create `scripts/backup.ps1` to archive the SQLite database, ChromaDB vector store, and uploaded documents.
- **Action**: Create `scripts/restore.ps1` to safely restore from archived zips.
- **Action**: Create helper scripts like `scripts/start.ps1`, `scripts/stop.ps1`, and `scripts/reset.ps1`.

### 6. Static Analysis & Testing
- **Action**: Setup `pre-commit` hooks and configure `black`, `isort`, `flake8`, and `mypy` in `pyproject.toml`.

### 7. Documentation
- **Action**: Update the root `README.md` and create `docs/deployment.md`, `docs/architecture.md`, and `docs/developer_guide.md`.
