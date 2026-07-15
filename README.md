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

## Current Progress
- **Phase 1 (Enterprise Project Setup):** Complete. Modular Django/FastAPI and React/Vite layout, Docker configurations.
- **Phase 2 (Agentic AI Core Infrastructure):** Complete. Implemented task manager, execution manager, workflow engine, state management, and memory interfaces.
- **Phase 3 (AI Intelligence Layer):** Complete. Implemented Ollama LLM integration, Langchain/LangGraph structured parsing, ChromaDB vector store, Reasoning/Reflection engines, and SQLite-backed memory systems.
- **Phase 4 (Business Intelligence Agents):** Complete. Built Document, Website, Competitor, Marketing, SEO, Report, and QA agents with strict Pydantic output validation and LangGraph dynamic routing.
- **Phase 5 (Frontend Application):** Complete. Built a modern enterprise dashboard using React 19, Vite, Tailwind CSS, Zustand, and React Router to orchestrate the Master Agent and workflows.
