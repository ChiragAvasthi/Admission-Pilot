# AdmissionPilot - Phase 6: End-to-End Integration Implementation Plan

This document outlines the architecture and implementation strategy for integrating the Backend AI Core with the Frontend Dashboard into a seamless, end-to-end production application (Phase 6).

## Final Decisions
- **Database Schema**: Managed strictly through Alembic migrations using SQLAlchemy. Tables will not auto-create on startup.
- **File Processing**: The Upload endpoint will only store files and metadata. Chunking and vectorization (ChromaDB) will be executed asynchronously as the first step of the Agent Execution workflow to avoid HTTP timeouts.

## Proposed Changes

### 1. Backend Core Setup
- **Action**: Create `backend/app/main.py` configuring FastAPI, CORS, and API routers.
- **Action**: Create `backend/app/db/` with `database.py` and `base.py`.
- **Action**: Create SQLAlchemy models in `backend/app/models/` for `Organization`, `Project`, `Upload`, `Execution`, and `Report`.
- **Action**: Create Pydantic schemas in `backend/app/schemas/` for request/response validation.
- **Action**: Set up Alembic and generate the initial schema migration.

### 2. Backend API Endpoints (FastAPI)
- **Organizations & Projects**: CRUD endpoints in `backend/app/api/v1/endpoints/organizations.py` and `projects.py`.
- **Uploads**: Create `backend/app/api/v1/endpoints/uploads.py` to handle `UploadFile`, save to disk, and store metadata in the DB.
- **Execution**: Create `backend/app/api/v1/endpoints/execution.py` to trigger the `MasterAgent` in a FastAPI `BackgroundTask`.
- **Reports**: Create `backend/app/api/v1/endpoints/reports.py` to fetch generated markdown reports.

### 3. Real-Time WebSockets
- **Action**: Create `backend/app/api/v1/websockets/execution_ws.py` to manage active connections.
- **Action**: Connect the existing `EventDispatcher` to the WebSocket manager so agent transitions stream instantly to connected clients.

### 4. Frontend Integration
- **Action**: Update `frontend/src/services/api.ts` to include strongly typed hooks/functions for all endpoints.
- **Action**: Wire up `Organizations.tsx` and `Projects.tsx` forms to create actual records.
- **Action**: Wire up `Uploads.tsx` to push multipart form data to the backend.
- **Action**: Overhaul `Execution.tsx` to connect to the WebSocket and render live timelines.
- **Action**: Wire up `Reports.tsx` to fetch the real generated report from the DB.

### 5. Documentation & E2E Testing
- **Action**: Write an end-to-end Python script validating the entire flow from Org creation to Report generation.
- **Action**: Generate `docs/integration.md` with sequence diagrams, system flow, and architecture explanations.
