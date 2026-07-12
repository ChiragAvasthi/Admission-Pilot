from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List
from app.agents.types import WorkflowStatus

class PlanningState(BaseModel):
    goal: str
    status: WorkflowStatus = WorkflowStatus.PLANNING
    capabilities_required: List[str] = Field(default_factory=list)
    plan_id: Optional[str] = None

class ExecutionState(BaseModel):
    plan_id: str
    status: WorkflowStatus = WorkflowStatus.EXECUTING
    completed_tasks: int = 0
    total_tasks: int = 0
    current_task_id: Optional[str] = None
    errors: List[str] = Field(default_factory=list)

class ReviewState(BaseModel):
    execution_results: Dict[str, Any] = Field(default_factory=dict)
    status: WorkflowStatus = WorkflowStatus.REVIEWING
    approved: bool = False
    feedback: Optional[str] = None

class CompletedState(BaseModel):
    status: WorkflowStatus = WorkflowStatus.COMPLETED
    final_output: Any
    metrics: Dict[str, Any] = Field(default_factory=dict)
