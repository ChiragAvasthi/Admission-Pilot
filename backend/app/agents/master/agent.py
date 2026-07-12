import logging
from typing import Any, Dict
from app.agents.base.agent import BaseAgent
from app.agents.planner.planner import Planner
from app.agents.execution.manager import ExecutionManager
from app.agents.state.context import ContextManager

logger = logging.getLogger(__name__)

class MasterAgent(BaseAgent):
    def __init__(self, agent_id: str, planner: Planner, execution_manager: ExecutionManager):
        super().__init__(
            agent_id=agent_id,
            name="MasterAgent",
            description="Orchestrates planning and execution of user requests.",
            capabilities=["ORCHESTRATION"]
        )
        self.planner = planner
        self.execution_manager = execution_manager

    def initialize(self) -> None:
        logger.info("MasterAgent initialized.")

    def execute(self, task_input: Dict[str, Any], context_manager: ContextManager) -> Any:
        """
        Receives user request, calls planner, executes plan, and generates final response.
        """
        goal = task_input.get("goal")
        if not goal:
            raise ValueError("Goal is required for MasterAgent execution.")
            
        logger.info(f"MasterAgent processing goal: {goal}")
        
        # 1. Planning
        plan = self.planner.generate_plan(goal, context_manager)
        
        # 2. Execution
        execution_results = self.execution_manager.execute_plan(plan, context_manager)
        
        # 3. Review & Merge Outputs (Simplified for core structure)
        final_output = self._merge_outputs(execution_results)
        
        # 4. Generate Response
        return self.generate_response(final_output)

    def _merge_outputs(self, results: Dict[str, Any]) -> str:
        """Merges outputs from various executed tasks."""
        if not results:
            return "No results produced."
        return " | ".join(f"{k}: {v}" for k, v in results.items())
