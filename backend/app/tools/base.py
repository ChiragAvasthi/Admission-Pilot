from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """
    Abstract base class for all tools in the framework.
    """
    name: str = "BaseTool"
    description: str = "A basic tool."

    @abstractmethod
    def run(self, **kwargs) -> Any:
        """
        Execute the tool's core logic.
        """
        pass
        
    async def arun(self, **kwargs) -> Any:
        """
        Async execution of the tool's core logic. 
        Defaults to synchronous run if not overridden.
        """
        return self.run(**kwargs)

    def get_info(self) -> Dict[str, str]:
        """
        Returns information about the tool for LLM context.
        """
        return {
            "name": self.name,
            "description": self.description
        }
