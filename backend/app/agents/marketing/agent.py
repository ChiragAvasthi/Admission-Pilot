import time
import logging
from typing import Any, Dict
from app.agents.base.agent import BaseAgent
from app.agents.types import Capability, AgentStatus
from app.agents.state.context import ContextManager
from app.parsers.agents import MarketingStrategyResult
from app.llm.model_manager import ModelManager
from app.agents.prompts.manager import PromptManager
from app.knowledge.store import KnowledgeStore

logger = logging.getLogger(__name__)

class MarketingStrategyAgent(BaseAgent):
    def __init__(self, model_manager: ModelManager, knowledge_store: KnowledgeStore):
        super().__init__(
            agent_id="agent_marketing_01",
            name="Marketing Strategy Agent",
            description="Generates admission and marketing strategies.",
            capabilities=[Capability.MARKETING_STRATEGY]
        )
        self.model_manager = model_manager
        self.knowledge_store = knowledge_store
        self.prompt_manager = PromptManager()

    def initialize(self) -> None:
        self.status = AgentStatus.IDLE

    def execute(self, task_input: Dict[str, Any], context_manager: ContextManager) -> MarketingStrategyResult:
        start_time = time.time()
        self.status = AgentStatus.BUSY
        
        try:
            # Query knowledge base for past campaigns and competitor data
            historical_data = self.knowledge_store.query_knowledge("past campaigns competitor data")
            
            prompt = self.prompt_manager.load_prompt(
                "marketing_agent.md", 
                historical_data=historical_data,
                context=context_manager.get_context().model_dump_json()
            )
            
            llm = self.model_manager.get_active_model()
            result: MarketingStrategyResult = llm.structured_invoke(
                prompt=prompt,
                schema=MarketingStrategyResult
            )
            
            self.confidence = result.confidence_score
            self.log_execution(start_time, task_input, result)
            return result
            
        except Exception as e:
            self.log_execution(start_time, task_input, None, error=e)
            raise

    def validate_output(self, output: Any) -> bool:
        return isinstance(output, MarketingStrategyResult)
