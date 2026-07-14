import time
import logging
from typing import Any, Dict
from app.agents.base.agent import BaseAgent
from app.agents.types import Capability, AgentStatus
from app.agents.state.context import ContextManager
from app.parsers.agents import WebsiteAuditResult
from app.llm.model_manager import ModelManager
from app.agents.prompts.manager import PromptManager

logger = logging.getLogger(__name__)

class WebsiteAnalysisAgent(BaseAgent):
    def __init__(self, model_manager: ModelManager):
        super().__init__(
            agent_id="agent_web_audit_01",
            name="Website Analysis Agent",
            description="Analyzes website structure, navigation, and UX.",
            capabilities=[Capability.WEBSITE_ANALYSIS]
        )
        self.model_manager = model_manager
        self.prompt_manager = PromptManager()

    def initialize(self) -> None:
        self.status = AgentStatus.IDLE

    def validate_input(self, task_input: Dict[str, Any]) -> bool:
        return "url" in task_input

    def execute(self, task_input: Dict[str, Any], context_manager: ContextManager) -> WebsiteAuditResult:
        start_time = time.time()
        self.status = AgentStatus.BUSY
        
        try:
            url = task_input["url"]
            # Mocking website scraping tool invocation
            scraped_content = f"Mocked scraped HTML structure and metadata from {url}"
            
            prompt = self.prompt_manager.load_prompt(
                "website_agent.md", 
                url=url,
                scraped_content=scraped_content,
                context=context_manager.get_context().model_dump_json()
            )
            
            llm = self.model_manager.get_active_model()
            result: WebsiteAuditResult = llm.structured_invoke(
                prompt=prompt,
                schema=WebsiteAuditResult
            )
            
            self.confidence = result.confidence_score
            self.log_execution(start_time, task_input, result)
            return result
            
        except Exception as e:
            self.log_execution(start_time, task_input, None, error=e)
            raise

    def validate_output(self, output: Any) -> bool:
        return isinstance(output, WebsiteAuditResult)
