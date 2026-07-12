from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid
from app.agents.types import TaskStatus, Priority

class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    assigned_agent: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    created_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    started_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
    confidence: float = 0.0
    dependencies: List[str] = Field(default_factory=list)
    retry_count: int = 0
    execution_log: List[Dict[str, Any]] = Field(default_factory=list)
    input_data: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None

class TaskManager:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def create_task(self, name: str, description: str, dependencies: Optional[List[str]] = None, **kwargs) -> Task:
        task = Task(name=name, description=description, dependencies=dependencies or [], **kwargs)
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def update_status(self, task_id: str, status: TaskStatus) -> Optional[Task]:
        task = self.get_task(task_id)
        if task:
            task.status = status
            if status == TaskStatus.IN_PROGRESS and not task.started_time:
                task.started_time = datetime.now(timezone.utc)
            elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                task.completed_time = datetime.now(timezone.utc)
        return task

    def assign_agent(self, task_id: str, agent_id: str) -> Optional[Task]:
        task = self.get_task(task_id)
        if task:
            task.assigned_agent = agent_id
        return task

    def track_progress(self, task_id: str, log_entry: Dict[str, Any]) -> None:
        task = self.get_task(task_id)
        if task:
            log_entry['timestamp'] = datetime.now(timezone.utc).isoformat()
            task.execution_log.append(log_entry)

    def retry_failed_task(self, task_id: str) -> Optional[Task]:
        task = self.get_task(task_id)
        if task and task.status == TaskStatus.FAILED:
            task.retry_count += 1
            task.status = TaskStatus.PENDING
            task.error = None
            task.completed_time = None
        return task

    def cancel_task(self, task_id: str) -> Optional[Task]:
        return self.update_status(task_id, TaskStatus.CANCELLED)

    def get_pending_tasks(self) -> List[Task]:
        """Returns tasks that are pending and have their dependencies met."""
        completed_ids = {t.id for t in self._tasks.values() if t.status == TaskStatus.COMPLETED}
        return [
            t for t in self._tasks.values() 
            if t.status == TaskStatus.PENDING and all(d in completed_ids for d in t.dependencies)
        ]
