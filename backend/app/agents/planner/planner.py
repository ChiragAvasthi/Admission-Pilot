import logging
from typing import Dict, Any, List
from app.agents.planner.models import ExecutionPlan
from app.agents.state.context import ContextManager
from app.agents.registry.registry import AgentRegistry
from app.llm.model_manager import ModelManager
from app.agents.prompts.manager import PromptManager
from app.parsers.structured import StructuredExecutionPlan

logger = logging.getLogger(__name__)

class Planner:
    def __init__(self, agent_registry: AgentRegistry, model_manager: ModelManager):
        self.agent_registry = agent_registry
        self.model_manager = model_manager
        self.prompt_manager = PromptManager()

    def generate_plan(self, goal: str, context: ContextManager) -> ExecutionPlan:
        """
        Uses the LLM to dynamically generate an execution plan based on the goal.
        """
        logger.info(f"LLM Planner generating execution plan for goal: {goal}")
        
        ctx_data = context.get_context().model_dump_json()
        prompt = self.prompt_manager.load_prompt("planner_prompt.txt", goal=goal, context=ctx_data)
        llm = self.model_manager.get_active_model()
        
        try:
            structured_plan: StructuredExecutionPlan = llm.structured_invoke(
                prompt=prompt,
                schema=StructuredExecutionPlan
            )
            
            # Convert structured plan to internal ExecutionPlan format
            tasks_dict = [
                {
                    "name": t.name,
                    "description": t.description,
                    "priority": t.priority.value,
                    "dependencies": t.dependencies
                }
                for t in structured_plan.tasks
            ]
            
            plan = ExecutionPlan(
                goal=structured_plan.goal,
                required_agents=structured_plan.required_agents,
                tasks=tasks_dict,
                expected_output=structured_plan.expected_output
            )
            
            logger.info(f"Generated LLM ExecutionPlan {plan.id} with {len(tasks_dict)} tasks.")
            return plan
            
        except Exception as e:
            logger.error(f"Planner failed to generate plan: {e}")
            raise
