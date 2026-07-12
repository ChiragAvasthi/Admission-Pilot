import logging
from typing import Any, Dict
from app.agents.planner.models import ExecutionPlan
from app.agents.workflow.engine import WorkflowEngine
from app.agents.state.context import ContextManager
from app.agents.registry.registry import AgentRegistry
from app.agents.events.dispatcher import EventDispatcher

logger = logging.getLogger(__name__)

class ExecutionManager:
    def __init__(self, workflow_engine: WorkflowEngine, agent_registry: AgentRegistry, event_dispatcher: EventDispatcher):
        self.workflow_engine = workflow_engine
        self.agent_registry = agent_registry
        self.event_dispatcher = event_dispatcher

    def execute_plan(self, plan: ExecutionPlan, context_manager: ContextManager) -> Dict[str, Any]:
        """
        Executes a plan by orchestrating tasks through the workflow engine and dispatching to agents.
        """
        logger.info(f"ExecutionManager starting plan {plan.id}")
        self.workflow_engine.receive_plan(plan)
        self.workflow_engine.execute()
        
        # In a real async/event-driven implementation, this would be handled via task queues.
        # For this core structure, we simulate a synchronous execution loop.
        while pending_tasks := self.workflow_engine.task_manager.get_pending_tasks():
            for task in pending_tasks:
                # Naive agent assignment: find any agent, or just use master/default
                agent = None
                if task.assigned_agent:
                    agent = self.agent_registry.get_agent(task.assigned_agent)
                if not agent:
                    # Just grab the first available for the simulation
                    available = self.agent_registry.get_available_agents()
                    if available:
                        agent = available[0]
                
                if agent:
                    logger.info(f"Executing task {task.id} using agent {agent.name}")
                    try:
                        # Update context before execution
                        context_manager.update_context({"current_task": task.name})
                        
                        # Execute
                        result = agent.execute({"task": task.description}, context_manager)
                        
                        # Update context after execution
                        context_manager.update_context({f"task_{task.id}_result": result})
                        
                        # Track success
                        self.workflow_engine.track_task_completion(task.id, result)
                    except Exception as e:
                        logger.error(f"Task {task.id} failed: {str(e)}")
                        self.workflow_engine.track_task_failure(task.id, str(e))
                else:
                    logger.error(f"No agent available for task {task.id}")
                    self.workflow_engine.track_task_failure(task.id, "No available agent")

        logger.info(f"ExecutionManager finished plan {plan.id}")
        return self.workflow_engine.results
