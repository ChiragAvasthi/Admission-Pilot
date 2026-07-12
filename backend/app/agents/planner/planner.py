import logging
from typing import Dict, Any, List
from app.agents.planner.models import ExecutionPlan
from app.agents.state.context import ContextManager
from app.agents.registry.registry import AgentRegistry

logger = logging.getLogger(__name__)

class Planner:
    def __init__(self, agent_registry: AgentRegistry):
        self.agent_registry = agent_registry

    def generate_plan(self, goal: str, context: ContextManager) -> ExecutionPlan:
        """
        Analyzes the goal and current context to generate an execution plan.
        In a full implementation, this would involve calling an LLM.
        For this core infrastructure, we return a mock plan structure.
        """
        logger.info(f"Generating execution plan for goal: {goal}")
        
        # Example of how planner would identify capabilities
        required_capabilities = ["RESEARCH", "WRITING"]
        
        # Select agents
        selected_agents = []
        for cap in required_capabilities:
            agents = self.agent_registry.filter_by_capability(cap)
            if agents:
                selected_agents.append(agents[0].id)
                
        # Construct Mock Plan
        tasks = [
            {
                "name": "Analyze Requirements",
                "description": f"Analyze the goal: {goal}",
                "priority": "HIGH",
                "dependencies": []
            },
            {
                "name": "Execute Core Logic",
                "description": "Perform the required actions based on analysis",
                "priority": "MEDIUM",
                "dependencies": ["Analyze Requirements"]
            }
        ]
        
        plan = ExecutionPlan(
            goal=goal,
            required_agents=selected_agents,
            tasks=tasks,
            expected_output="Final synthesized response based on goal."
        )
        
        logger.info(f"Generated ExecutionPlan {plan.id} with {len(tasks)} tasks.")
        return plan
