# Class Diagram

## 1. Diagram Name
Class Diagram - Domain Data Models

## 2. Purpose of the diagram
To document the static structure of the database and application domain models, illustrating the classes, their attributes, methods, and relationships.

## 3. What the diagram represents
This diagram represents the actual SQLAlchemy ORM domain models defined in the FastAPI backend (`backend/app/models/domain.py`), which maps directly to the SQLite database schema. It also logically connects the `ExecutionManager` to these entities.

## 4. Key elements shown
*   **Classes:** `Organization`, `Project`, `Upload`, `Execution`, `Report`, `ExecutionManager`.
*   **Attributes:** Relevant fields with their data types (e.g., `String`, `Text`, `DateTime`, `JSON`).
*   **Methods:** Base repository/manager logic representations.
*   **Relationships:** 
    * One-to-Many: Organization -> Project, Project -> Upload, Project -> Execution.
    * One-to-One: Execution -> Report.
    * Dependency: ExecutionManager interacts with Execution and Report.

## 5. Brief explanation of the workflow/relationships
The `Organization` serves as the root tenant for the system, which can contain multiple `Project`s. A `Project` acts as an encapsulation unit for uploaded documents (`Upload`) and AI workflow runs (`Execution`). When an `Execution` runs, it generates one final `Report`. The `ExecutionManager` is the core service class that orchestrates the status updates and creation of these entities during runtime.

---

### Mermaid Source

```mermaid
classDiagram
    class Organization {
        +String id
        +String name
        +Text description
        +DateTime created_at
        +DateTime updated_at
        +create(org_in) Organization
        +list_all() List~Organization~
    }

    class Project {
        +String id
        +String organization_id
        +String name
        +Text description
        +String website_url
        +String status
        +DateTime created_at
        +DateTime updated_at
        +create(project_in) Project
        +list_by_org(organization_id) List~Project~
    }

    class Upload {
        +String id
        +String project_id
        +String filename
        +String file_path
        +String content_type
        +String status
        +DateTime created_at
        +DateTime updated_at
        +upload_file(project_id, file) Upload
        +list_by_project(project_id) List~Upload~
    }

    class Execution {
        +String id
        +String project_id
        +String status
        +String progress
        +JSON logs
        +DateTime created_at
        +DateTime updated_at
        +DateTime completed_at
        +start(project_id) Execution
        +get_by_id(execution_id) Execution
        +update_status(status) void
    }

    class Report {
        +String id
        +String execution_id
        +String project_id
        +String title
        +Text content
        +DateTime created_at
        +list_by_project(project_id) List~Report~
        +get_by_id(report_id) Report
    }

    class ExecutionManager {
        +run_execution_workflow(execution_id, project_id) void
        +broadcast_update(execution_id, payload) void
    }

    Organization "1" -- "*" Project : has
    Project "1" -- "*" Upload : contains
    Project "1" -- "*" Execution : runs
    Execution "1" -- "1" Report : generates

    ExecutionManager ..> Execution : manages
    ExecutionManager ..> Report : creates
```
