import time
import logging
from typing import Any, Dict
from app.agents.base.agent import BaseAgent
from app.agents.types import Capability, AgentStatus
from app.agents.state.context import ContextManager
from app.parsers.agents import ReportResult
from app.llm.model_manager import ModelManager
from app.agents.prompts.manager import PromptManager

logger = logging.getLogger(__name__)

class ReportGenerationAgent(BaseAgent):
    def __init__(self, model_manager: ModelManager):
        super().__init__(
            agent_id="agent_report_01",
            name="Report Generation Agent",
            description="Merges agent outputs into a comprehensive final report.",
            capabilities=[Capability.REPORT_GENERATION]
        )
        self.model_manager = model_manager
        self.prompt_manager = PromptManager()

    def initialize(self) -> None:
        self.status = AgentStatus.IDLE

    def execute(self, task_input: Dict[str, Any], context_manager: ContextManager) -> ReportResult:
        start_time = time.time()
        self.status = AgentStatus.BUSY
        
        try:
            # Report agent expects multiple analysis results in the task input or context
            all_reports = task_input.get("agent_outputs", {})
            
            prompt = self.prompt_manager.load_prompt(
                "report_agent.md", 
                agent_outputs=str(all_reports),
                context=context_manager.get_context().model_dump_json()
            )
            
            llm = self.model_manager.get_active_model()
            result: ReportResult = llm.structured_invoke(
                prompt=prompt,
                schema=ReportResult
            )
            
            self.confidence = result.confidence_score
            self.log_execution(start_time, task_input, result)
            return result
            
        except Exception as e:
            self.log_execution(start_time, task_input, None, error=e)
            raise

    def validate_output(self, output: Any) -> bool:
        return isinstance(output, ReportResult)
