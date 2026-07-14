import time
import logging
from typing import Any, Dict
from app.agents.base.agent import BaseAgent
from app.agents.types import Capability, AgentStatus
from app.agents.state.context import ContextManager
from app.parsers.agents import CompetitorAnalysisResult
from app.llm.model_manager import ModelManager
from app.agents.prompts.manager import PromptManager

logger = logging.getLogger(__name__)

class CompetitorIntelligenceAgent(BaseAgent):
    def __init__(self, model_manager: ModelManager):
        super().__init__(
            agent_id="agent_comp_intel_01",
            name="Competitor Intelligence Agent",
            description="Identifies competitors and compares metrics.",
            capabilities=[Capability.COMPETITOR_INTELLIGENCE]
        )
        self.model_manager = model_manager
        self.prompt_manager = PromptManager()

    def initialize(self) -> None:
        self.status = AgentStatus.IDLE

    def validate_input(self, task_input: Dict[str, Any]) -> bool:
        return "college_name" in task_input and "location" in task_input

    def execute(self, task_input: Dict[str, Any], context_manager: ContextManager) -> CompetitorAnalysisResult:
        start_time = time.time()
        self.status = AgentStatus.BUSY
        
        try:
            # Mocking search interface
            search_data = f"Mocked competitor data for {task_input['college_name']} in {task_input['location']}"
            
            prompt = self.prompt_manager.load_prompt(
                "competitor_agent.md", 
                search_data=search_data,
                context=context_manager.get_context().model_dump_json()
            )
            
            llm = self.model_manager.get_active_model()
            result: CompetitorAnalysisResult = llm.structured_invoke(
                prompt=prompt,
                schema=CompetitorAnalysisResult
            )
            
            self.confidence = result.confidence_score
            self.log_execution(start_time, task_input, result)
            return result
            
        except Exception as e:
            self.log_execution(start_time, task_input, None, error=e)
            raise

    def validate_output(self, output: Any) -> bool:
        return isinstance(output, CompetitorAnalysisResult)
