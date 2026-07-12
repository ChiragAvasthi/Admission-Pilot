from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid
from app.agents.types import Priority

class ExecutionPlan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    goal: str
    required_agents: List[str] = Field(default_factory=list)
    tasks: List[Dict[str, Any]] = Field(default_factory=list)
    priority: Priority = Priority.MEDIUM
    dependencies_graph: Dict[str, List[str]] = Field(default_factory=dict)
    expected_output: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
