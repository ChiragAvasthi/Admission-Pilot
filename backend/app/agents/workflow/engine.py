import logging
from typing import Any, Dict, List, Optional
from app.agents.types import WorkflowStatus, TaskStatus
from app.agents.workflow.task import TaskManager, Task
from app.agents.planner.models import ExecutionPlan
from app.agents.events.dispatcher import EventDispatcher
from app.agents.events.models import WorkflowStarted, WorkflowCompleted, TaskCreated, TaskStarted, TaskCompleted, TaskFailed

logger = logging.getLogger(__name__)

class WorkflowEngine:
    def __init__(self, task_manager: TaskManager, event_dispatcher: EventDispatcher):
        self.task_manager = task_manager
        self.event_dispatcher = event_dispatcher
        self.status = WorkflowStatus.INITIALIZED
        self.plan: Optional[ExecutionPlan] = None
        self.results: Dict[str, Any] = {}

    def receive_plan(self, plan: ExecutionPlan) -> None:
        self.plan = plan
        for task_def in plan.tasks:
            task = self.task_manager.create_task(
                name=task_def.get("name", "Unnamed Task"),
                description=task_def.get("description", ""),
                dependencies=task_def.get("dependencies", []),
                priority=task_def.get("priority", "MEDIUM")
            )
            self.event_dispatcher.dispatch(TaskCreated(task_id=task.id, task_name=task.name))
        logger.info(f"WorkflowEngine received plan with {len(plan.tasks)} tasks.")

    def execute(self) -> None:
        """Starts the workflow execution loop."""
        if not self.plan:
            raise ValueError("Cannot execute without a plan.")
        
        self.status = WorkflowStatus.EXECUTING
        self.event_dispatcher.dispatch(WorkflowStarted(workflow_id=self.plan.id, goal="Executing plan"))
        logger.info(f"Workflow {self.plan.id} started execution.")

    def pause(self) -> None:
        if self.status == WorkflowStatus.EXECUTING:
            self.status = WorkflowStatus.PAUSED
            logger.info("Workflow paused.")

    def resume(self) -> None:
        if self.status == WorkflowStatus.PAUSED:
            self.status = WorkflowStatus.EXECUTING
            logger.info("Workflow resumed.")

    def cancel(self) -> None:
        self.status = WorkflowStatus.CANCELLED
        logger.info("Workflow cancelled.")
        
    def track_task_completion(self, task_id: str, result: Any) -> None:
        task = self.task_manager.update_status(task_id, TaskStatus.COMPLETED)
        if task:
            task.result = result
            self.results[task_id] = result
            self.event_dispatcher.dispatch(TaskCompleted(task_id=task_id, result=result))
            self._check_workflow_completion()

    def track_task_failure(self, task_id: str, error: str) -> None:
        task = self.task_manager.update_status(task_id, TaskStatus.FAILED)
        if task:
            task.error = error
            self.event_dispatcher.dispatch(TaskFailed(task_id=task_id, error=error))
            self.status = WorkflowStatus.FAILED
            logger.error(f"Workflow failed due to task {task_id}")

    def _check_workflow_completion(self) -> None:
        pending = self.task_manager.get_pending_tasks()
        in_progress = [t for t in self.task_manager._tasks.values() if t.status == TaskStatus.IN_PROGRESS]
        
        if not pending and not in_progress and self.status == WorkflowStatus.EXECUTING:
            self.status = WorkflowStatus.COMPLETED
            self.event_dispatcher.dispatch(WorkflowCompleted(workflow_id=self.plan.id if self.plan else "unknown", final_output=self.results))
            logger.info("Workflow execution completed successfully.")
