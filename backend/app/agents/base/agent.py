from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import time
import logging
from app.agents.types import AgentStatus
from app.agents.state.context import ContextManager

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str, description: str, capabilities: List[str]):
        self.id = agent_id
        self.name = name
        self.description = description
        self.capabilities = capabilities
        self.status = AgentStatus.IDLE
        self.confidence = 1.0
        self.execution_time = 0.0

    @abstractmethod
    def initialize(self) -> None:
        """Initialize any resources needed by the agent."""
        pass

    @abstractmethod
    def execute(self, task_input: Dict[str, Any], context_manager: ContextManager) -> Any:
        """Execute the agent's primary capability."""
        pass

    def validate_input(self, task_input: Dict[str, Any]) -> bool:
        """Validate input before execution."""
        return True

    def validate_output(self, output: Any) -> bool:
        """Validate output after execution."""
        return True

    def generate_response(self, result: Any) -> str:
        """Format the result into a standardized response."""
        return str(result)

    def log_execution(self, start_time: float, task_input: Any, result: Any, error: Optional[Exception] = None) -> None:
        """Log execution details, timing, and errors."""
        self.execution_time = time.time() - start_time
        if error:
            self.status = AgentStatus.ERROR
            logger.error(f"Agent {self.name} failed in {self.execution_time:.2f}s: {error}")
        else:
            self.status = AgentStatus.IDLE
            logger.info(f"Agent {self.name} completed successfully in {self.execution_time:.2f}s")

    def health_check(self) -> bool:
        """Check if the agent is healthy and ready to accept tasks."""
        return self.status != AgentStatus.OFFLINE
