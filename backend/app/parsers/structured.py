from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.agents.types import Priority

class ReasoningResult(BaseModel):
    goal_understanding: str = Field(description="The agent's understanding of the original goal.")
    missing_information: List[str] = Field(description="List of information or context currently missing.")
    required_capabilities: List[str] = Field(description="List of agent capabilities required to achieve this goal.")
    execution_strategy: str = Field(description="Step-by-step strategy to execute the goal.")
    confidence_score: float = Field(description="Confidence score from 0.0 to 1.0 on being able to achieve the goal.")

class ReflectionResult(BaseModel):
    is_consistent: bool = Field(description="Whether the output is consistent with the goal and context.")
    detected_hallucinations: List[str] = Field(description="List of potential hallucinations or incorrect assumptions detected.")
    confidence_score: float = Field(description="Confidence score of the evaluation.")
    needs_regeneration: bool = Field(description="True if the response is too flawed and needs regeneration.")
    feedback: str = Field(description="Constructive feedback to improve the response if regeneration is needed.")

class ToolCall(BaseModel):
    tool_name: str = Field(description="The name of the tool to invoke.")
    arguments: Dict[str, Any] = Field(description="The arguments to pass to the tool.")

class TaskPlan(BaseModel):
    name: str = Field(description="Name of the task.")
    description: str = Field(description="Detailed description of what the task must accomplish.")
    priority: Priority = Field(description="Priority of the task.")
    dependencies: List[str] = Field(default_factory=list, description="List of task names that must be completed before this task.")

class StructuredExecutionPlan(BaseModel):
    goal: str = Field(description="The overall goal.")
    tasks: List[TaskPlan] = Field(description="The ordered list of tasks to execute.")
    required_agents: List[str] = Field(description="The list of agent capabilities required.")
    expected_output: str = Field(description="Description of the final expected output.")
