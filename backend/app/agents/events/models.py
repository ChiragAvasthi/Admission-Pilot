from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from datetime import datetime, timezone
import uuid

class BaseEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TaskCreated(BaseEvent):
    task_id: str
    task_name: str

class TaskStarted(BaseEvent):
    task_id: str
    agent_id: str

class TaskCompleted(BaseEvent):
    task_id: str
    result: Any

class TaskFailed(BaseEvent):
    task_id: str
    error: str

class AgentRegistered(BaseEvent):
    agent_id: str
    agent_name: str
    capabilities: list[str]

class WorkflowStarted(BaseEvent):
    workflow_id: str
    goal: str

class WorkflowCompleted(BaseEvent):
    workflow_id: str
    final_output: Any

class ContextUpdated(BaseEvent):
    updates: Dict[str, Any]

class AgentStarted(BaseEvent):
    agent_name: str
    task_id: str

class AgentCompleted(BaseEvent):
    agent_name: str
    task_id: str

class AgentFailed(BaseEvent):
    agent_name: str
    task_id: str
    error: str

class RevisionRequested(BaseEvent):
    task_id: str
    reason: str

class ReportGenerated(BaseEvent):
    report_id: str
    summary: str
