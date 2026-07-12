import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class Context(BaseModel):
    company: Optional[str] = None
    project: Optional[str] = None
    goal: str
    budget: Optional[float] = None
    website: Optional[str] = None
    uploaded_files: List[str] = Field(default_factory=list)
    extracted_information: Dict[str, Any] = Field(default_factory=dict)
    competitors: List[str] = Field(default_factory=list)
    agent_outputs: Dict[str, Any] = Field(default_factory=dict)
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    temporary_variables: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        frozen = True  # Context should be immutable unless updated through ContextManager


class ContextManager:
    def __init__(self, initial_context: Context):
        self._context = initial_context

    def get_context(self) -> Context:
        return self._context

    def update_context(self, updates: Dict[str, Any]) -> Context:
        """
        Creates a new Context object with the applied updates to maintain immutability.
        """
        current_data = self._context.model_dump()
        for key, value in updates.items():
            if key in current_data:
                if isinstance(current_data[key], dict) and isinstance(value, dict):
                    current_data[key].update(value)
                elif isinstance(current_data[key], list) and isinstance(value, list):
                    current_data[key].extend(value)
                else:
                    current_data[key] = value
            else:
                logger.warning(f"Key '{key}' not found in Context model. Storing in metadata.")
                current_data['metadata'][key] = value
        
        self._context = Context(**current_data)
        logger.info(f"Context updated with keys: {list(updates.keys())}")
        return self._context
