# AdmissionPilot - Architecture Overview

AdmissionPilot is a multi-tier, AI-native enterprise platform.

## 1. Frontend (Presentation Layer)
- **Framework**: React 19 + TypeScript + Vite.
- **Styling**: Tailwind CSS v4.
- **State Management**: Zustand (Global) + React Query (Server).
- **Key Features**: Real-time WebSocket connection to display LangGraph agent execution timelines and streaming logs.

## 2. Backend (API & Orchestration Layer)
- **Framework**: FastAPI (Python 3.11).
- **Concurrency**: Asynchronous `asyncio` loop for handling high-volume I/O, WebSockets, and background tasks.
- **Security**: `slowapi` for Rate Limiting, strict CORS policies, Max File Size middleware.
- **Database**: SQLite with `aiosqlite` and `SQLAlchemy`. Schema migrations managed strictly by `Alembic`.

## 3. Agentic AI Core (Intelligence Layer)
- **Orchestration**: `LangGraph` for defining cyclic and acyclic graph workflows for autonomous agents.
- **Vector DB**: `ChromaDB` for document chunking, embeddings, and RAG (Retrieval-Augmented Generation).
- **LLM**: Local-first inference using `Ollama` (default `qwen3:8b`).

## 4. Execution Flow
1. User uploads documents -> Saved to disk. Metadata saved to SQLite.
2. User clicks "Start Execution" -> HTTP POST to API.
3. API creates Execution record in SQLite -> Returns ID to user immediately.
4. API spawns Background Task -> Initiates `MasterAgent` LangGraph execution.
5. React connects to WebSocket (`/api/v1/ws/execution/{id}`).
6. As agents run, they dispatch events.
7. Backend pushes events via WebSocket -> React updates UI timeline in real-time.
