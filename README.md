# Admission Pilot

Enterprise-grade AI SaaS Platform.

## Project Structure

This repository is split into two entirely independent applications:

- `backend/`: Python FastAPI RESTful API.
- `frontend/`: React/Vite TypeScript Application.

## Getting Started

### Prerequisites
- Docker and Docker Compose (recommended for full stack)
- Python 3.10+ (for local backend development)
- Node.js 18+ (for local frontend development)

### Running with Docker (Recommended)

To spin up the entire stack (Database, Backend, Frontend):

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

### Local Development

Please refer to the detailed README files in each respective directory:
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
