import time
import logging
from typing import Any, Dict
from app.agents.base.agent import BaseAgent
from app.agents.types import Capability, AgentStatus
from app.agents.state.context import ContextManager
from app.parsers.agents import QAResult
from app.llm.model_manager import ModelManager
from app.agents.prompts.manager import PromptManager

logger = logging.getLogger(__name__)

class QualityAssuranceAgent(BaseAgent):
    def __init__(self, model_manager: ModelManager):
        super().__init__(
            agent_id="agent_qa_01",
            name="Quality Assurance Agent",
            description="Reviews generated reports and outputs for consistency.",
            capabilities=[Capability.QUALITY_ASSURANCE]
        )
        self.model_manager = model_manager
        self.prompt_manager = PromptManager()

    def initialize(self) -> None:
        self.status = AgentStatus.IDLE

    def execute(self, task_input: Dict[str, Any], context_manager: ContextManager) -> QAResult:
        start_time = time.time()
        self.status = AgentStatus.BUSY
        
        try:
            output_to_review = task_input.get("target_output", "Nothing provided")
            
            prompt = self.prompt_manager.load_prompt(
                "qa_agent.md", 
                target_output=output_to_review,
                context=context_manager.get_context().model_dump_json()
            )
            
            llm = self.model_manager.get_active_model()
            result: QAResult = llm.structured_invoke(
                prompt=prompt,
                schema=QAResult
            )
            
            # QA agent is strict. If confidence is below 0.8, force a revision.
            if result.confidence_score < 0.8:
                logger.warning(f"QA Agent flagged low confidence ({result.confidence_score}). Revision required.")
                result.needs_revision = True

            self.confidence = result.confidence_score
            self.log_execution(start_time, task_input, result)
            return result
            
        except Exception as e:
            self.log_execution(start_time, task_input, None, error=e)
            raise

    def validate_output(self, output: Any) -> bool:
        return isinstance(output, QAResult)
