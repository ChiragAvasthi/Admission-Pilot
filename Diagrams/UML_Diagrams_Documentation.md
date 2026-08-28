# Admission Pilot - UML Diagrams Documentation

This document contains the academic and technical explanations for the 8 UML diagrams generated for the **Admission Pilot** AI SaaS Platform. These descriptions correspond to the Mermaid source diagrams available in this directory.

---

## 1. Use Case Diagram
* **Purpose:** To visualize the functional requirements of the Admission Pilot system from the user's perspective, illustrating the interactions between the primary actors and the system's core functionalities.
* **What it represents:** This diagram represents the major use cases of the platform, including user actions such as managing organizations/projects, uploading documents, triggering AI workflows, and viewing generated reports.
* **Key elements shown:** Actor (User), System Boundary, core Use Cases (Manage Organizations, Execute AI Workflow), and relationships (associations, `<<include>>`, `<<extend>>`).
* **Brief explanation:** The User sets up their workspace (Organizations/Projects) and uploads documents. The core functionality is triggering the "Execute AI Workflow", which seamlessly includes background AI document processing. The user can optionally monitor the status in real-time via WebSockets and ultimately access the generated reports.

---

## 2. Activity Diagram
* **Purpose:** To illustrate the dynamic behavior of the system by depicting the control flow from one activity to another during the core AI execution process.
* **What it represents:** This diagram represents the step-by-step end-to-end workflow when a user triggers an AI analysis execution across the React frontend, FastAPI backend, and LangGraph-based Master Agent orchestration.
* **Key elements shown:** Initial/Final nodes, concurrent paths (WebSocket connection parallel to background execution), agent processing actions, and choice nodes for exception handling.
* **Brief explanation:** When the user clicks "Start Execution", an HTTP POST request initiates the workflow. The backend creates an execution record, returns the ID, and immediately forks the process: the frontend establishes a real-time WebSocket connection while the backend spawns a background task. The task initializes the LangGraph Master Agent which runs the intelligence pipeline (Document, Marketing, Report agents) and continuously broadcasts status updates to the UI.

---

## 3. Sequence Diagram
* **Purpose:** To illustrate how the different objects and components of the Admission Pilot system interact over time to accomplish the execution of the AI workflow.
* **What it represents:** This diagram shows the sequential message passing and function invocation between the User, React Frontend, FastAPI Backend, SQLite Database, WebSocket Manager, and the AI Core during execution.
* **Key elements shown:** Lifelines (User, UI, API, DB, WS Manager, AI Core), HTTP POST requests, DB transactions, background execution boundaries, and WebSocket events.
* **Brief explanation:** The sequence starts with the user interacting with the UI. The API processes the request, commits to SQLite, and replies to the UI. The UI connects to a WebSocket while the API spins up an async task. The AI LangGraph Core orchestrates the Ollama/ChromaDB integrations, periodically dispatching progress messages to the WebSocket Manager, which pushes them to the client.

---

## 4. Class Diagram
* **Purpose:** To document the static structure of the database and application domain models, illustrating the classes, their attributes, methods, and relationships.
* **What it represents:** This diagram maps the actual SQLAlchemy ORM models (`Organization`, `Project`, `Upload`, `Execution`, `Report`) found in the FastAPI backend, along with their core attributes and relationships.
* **Key elements shown:** Classes, strongly-typed attributes, and relationships such as One-to-Many (Organization to Project) and One-to-One (Execution to Report).
* **Brief explanation:** The `Organization` is the highest-level entity containing multiple `Project`s. Each `Project` encapsulates document `Upload`s and AI `Execution` runs. A successfully completed `Execution` generates a `Report`. The `ExecutionManager` acts as the service layer linking these models to background processing.

---

## 5. Component Diagram
* **Purpose:** To visualize the high-level software architecture, showing the major physical and logical components and how they interface with one another.
* **What it represents:** This diagram represents the modular architecture spanning the React frontend, the FastAPI backend, the AI intelligence layer, and the underlying databases.
* **Key elements shown:** Presentation Component (React/Zustand), API Component (FastAPI/WebSockets), Data Persistence (SQLite/ChromaDB), and the AI Core (LangGraph/Ollama).
* **Brief explanation:** The client interacts with the React app, which talks to FastAPI via REST and WebSockets. FastAPI manages SQLite data and routes heavy intelligence work to the LangGraph AI Engine. LangGraph securely interfaces with local ChromaDB vectors and the Ollama LLM to perform business logic without leaking data externally.

---

## 6. Deployment Diagram
* **Purpose:** To illustrate the physical deployment architecture showing how software components are mapped onto hardware/infrastructure nodes.
* **What it represents:** This diagram models the actual Docker Compose-based deployment structure of the platform, outlining containers, exposed ports, and communication protocols.
* **Key elements shown:** User Device (Browser), Docker Host Server, Container nodes (Frontend:3000, Backend:8000, Ollama), and persistent Docker Volumes.
* **Brief explanation:** The entire stack is containerized on a Docker Host. External HTTP/WS traffic hits the Frontend and Backend containers. Inside the secure Docker network, the Backend FastAPI application communicates with SQLite file volumes, ChromaDB containers, and the Ollama LLM runtime.

---

## 7. Communication Diagram
* **Purpose:** To show the structural organization of objects/components that send and receive messages during the AI Agent Execution Workflow.
* **What it represents:** A spatial view of the same interaction detailed in the Sequence Diagram, focusing on the structural links and chronologically numbered messages between system components.
* **Key elements shown:** Component nodes (React Client, API, DB, Background Task, Master Agent, WebSocket Manager) and numbered interaction links (1.0, 1.1... 4.0).
* **Brief explanation:** Communication flows outwards from the Client to the API (1.0). The API queries the Database (1.1, 1.2) and kicks off Background Tasks (1.4). The Client also connects directly to WebSockets (2.0). The Background Task triggers the Master Agent (3.0), which performs its duties (3.1) and pushes updates back out to the WebSocket Manager (3.2).

---

## 8. Object Diagram
* **Purpose:** To provide a concrete, realistic snapshot of the system's instantiated objects at a specific moment in time (post-execution).
* **What it represents:** This diagram takes the abstract models from the Class Diagram and fills them with realistic, related data representing an actual system state.
* **Key elements shown:** Instantiated objects with realistic sample values (e.g., `org1`, `proj1`, `exec1`) and their instance-level foreign key linkages.
* **Brief explanation:** This snapshot visualizes "Acme University" (`org1`) which has an active "Fall 2026 Strategy" project (`proj1`). The project has a completed document upload (`upload1`) and a finished AI workflow (`exec1`). The execution resulted in the creation of a tangible synthesis report (`report1`), correctly mapping abstract architecture to concrete runtime data.
