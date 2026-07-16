# AdmissionPilot Phase 6 Integration

## 1. System Flow Overview

AdmissionPilot integrates a React frontend, a FastAPI backend, an SQLite/SQLAlchemy database, and an autonomous LangGraph agent network.

```mermaid
graph TD
    User([User]) -->|HTTP / WebSockets| Frontend[React Dashboard]
    Frontend -->|REST API| API[FastAPI Backend]
    API -->|CRUD| DB[(SQLite DB)]
    API -->|Triggers| MasterAgent[Master Agent / LangGraph]
    MasterAgent -->|Delegates| SpecialistAgents[Business Agents]
    SpecialistAgents -->|Reads/Writes| Context[Shared Memory]
    SpecialistAgents -->|Retrieval| VectorStore[(ChromaDB)]
    MasterAgent -->|Real-time Updates| Dispatcher[Event Dispatcher]
    Dispatcher -->|WebSocket Messages| Frontend
```

## 2. API Flow

- **POST `/api/v1/organizations/`**: Create new client organization.
- **POST `/api/v1/projects/`**: Create a new admission drive project.
- **POST `/api/v1/uploads/`**: Upload PDFs, DOCX, CSV. Stores files in local directory and metadata in DB.
- **POST `/api/v1/execution/`**: Triggers the `MasterAgent` in a FastAPI `BackgroundTask`. Returns Execution ID immediately.
- **GET `/api/v1/reports/`**: Retrieve generated markdown reports for a project.

## 3. WebSocket Real-Time Flow

When the LangGraph workflow is running in the background, it continuously dispatches events to the WebSocket Manager.

```mermaid
sequenceDiagram
    participant React as Frontend Dashboard
    participant API as FastAPI Router
    participant WS as WebSocket Manager
    participant LangGraph as Master Agent
    
    React->>API: POST /api/v1/execution/
    API-->>React: 200 OK (Execution ID)
    React->>WS: Connect ws://.../api/v1/ws/execution/{id}
    WS-->>React: Connection Accepted
    
    API->>LangGraph: Start Background Task
    
    loop Every Agent Transition
        LangGraph->>WS: Broadcast Update Event
        WS-->>React: JSON Message (Status, Logs)
        React->>React: Update UI Timeline & Logs
    end
    
    LangGraph->>WS: Broadcast Complete Event
    WS-->>React: Final Message
```

## 4. Execution Flow details
The uploaded documents are **NOT** processed during the HTTP request to prevent timeouts. Instead, the first step of the LangGraph execution is the Document Intelligence Agent taking the raw files, chunking them, and inserting them into ChromaDB.
