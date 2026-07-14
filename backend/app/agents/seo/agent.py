import time
import logging
from typing import Any, Dict
from app.agents.base.agent import BaseAgent
from app.agents.types import Capability, AgentStatus
from app.agents.state.context import ContextManager
from app.parsers.agents import SEOResult
from app.llm.model_manager import ModelManager
from app.agents.prompts.manager import PromptManager
from app.knowledge.store import KnowledgeStore

logger = logging.getLogger(__name__)

class SEOStrategyAgent(BaseAgent):
    def __init__(self, model_manager: ModelManager, knowledge_store: KnowledgeStore):
        super().__init__(
            agent_id="agent_seo_01",
            name="SEO & Content Strategy Agent",
            description="Generates SEO keywords, metadata, and content plans.",
            capabilities=[Capability.SEO_STRATEGY]
        )
        self.model_manager = model_manager
        self.knowledge_store = knowledge_store
        self.prompt_manager = PromptManager()

    def initialize(self) -> None:
        self.status = AgentStatus.IDLE

    def execute(self, task_input: Dict[str, Any], context_manager: ContextManager) -> SEOResult:
        start_time = time.time()
        self.status = AgentStatus.BUSY
        
        try:
            # Query knowledge base for SEO context (website analysis)
            seo_context = self.knowledge_store.query_knowledge("website analysis seo metrics")
            
            prompt = self.prompt_manager.load_prompt(
                "seo_agent.md", 
                seo_context=seo_context,
                context=context_manager.get_context().model_dump_json()
            )
            
            llm = self.model_manager.get_active_model()
            result: SEOResult = llm.structured_invoke(
                prompt=prompt,
                schema=SEOResult
            )
            
            self.confidence = result.confidence_score
            self.log_execution(start_time, task_input, result)
            return result
            
        except Exception as e:
            self.log_execution(start_time, task_input, None, error=e)
            raise

    def validate_output(self, output: Any) -> bool:
        return isinstance(output, SEOResult)
