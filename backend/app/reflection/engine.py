import logging
from typing import Any
from app.llm.model_manager import ModelManager
from app.agents.prompts.manager import PromptManager
from app.parsers.structured import ReflectionResult

logger = logging.getLogger(__name__)

class ReflectionEngine:
    """
    Evaluates LLM outputs for consistency, hallucinations, and quality before proceeding.
    """
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.prompt_manager = PromptManager()

    def evaluate(self, goal: str, proposed_output: str) -> ReflectionResult:
        logger.info("ReflectionEngine evaluating output...")
        
        prompt = self.prompt_manager.load_prompt(
            "reflection_prompt.txt", 
            goal=goal, 
            proposed_output=proposed_output
        )
        llm = self.model_manager.get_active_model()
        
        try:
            result: ReflectionResult = llm.structured_invoke(
                prompt=prompt,
                schema=ReflectionResult
            )
            
            if result.needs_regeneration:
                logger.warning(f"Reflection requested regeneration. Feedback: {result.feedback}")
            else:
                logger.info(f"Reflection passed. Confidence: {result.confidence_score}")
                
            return result
        except Exception as e:
            logger.error(f"ReflectionEngine failed: {e}")
            raise
