import logging
from typing import Dict, Any
from app.llm.model_manager import ModelManager
from app.agents.prompts.manager import PromptManager
from app.parsers.structured import ReasoningResult

logger = logging.getLogger(__name__)

class ReasoningEngine:
    """
    The core brain of the platform. Evaluates requests, builds strategies, 
    and determines necessary agent capabilities.
    """
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.prompt_manager = PromptManager()

    def analyze_goal(self, request: str, context: str) -> ReasoningResult:
        logger.info("ReasoningEngine analyzing goal...")
        
        prompt = self.prompt_manager.load_prompt("reasoning_prompt.txt", request=request, context=context)
        llm = self.model_manager.get_active_model()
        
        try:
            # We enforce JSON output parsing to match ReasoningResult Pydantic schema
            result: ReasoningResult = llm.structured_invoke(
                prompt=prompt,
                schema=ReasoningResult
            )
            logger.info(f"Reasoning completed. Confidence: {result.confidence_score}")
            return result
        except Exception as e:
            logger.error(f"ReasoningEngine failed: {e}")
            raise
