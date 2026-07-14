import time
import logging
from typing import Any, Dict
from app.agents.base.agent import BaseAgent
from app.agents.types import Capability, AgentStatus
from app.agents.state.context import ContextManager
from app.parsers.agents import DocumentAnalysisResult
from app.llm.model_manager import ModelManager
from app.agents.prompts.manager import PromptManager
from app.knowledge.store import KnowledgeStore

logger = logging.getLogger(__name__)

class DocumentIntelligenceAgent(BaseAgent):
    def __init__(self, model_manager: ModelManager, knowledge_store: KnowledgeStore):
        super().__init__(
            agent_id="agent_doc_intel_01",
            name="Document Intelligence Agent",
            description="Extracts structured knowledge from documents and websites.",
            capabilities=[Capability.DOCUMENT_ANALYSIS]
        )
        self.model_manager = model_manager
        self.knowledge_store = knowledge_store
        self.prompt_manager = PromptManager()

    def initialize(self) -> None:
        self.status = AgentStatus.IDLE

    def validate_input(self, task_input: Dict[str, Any]) -> bool:
        return "document_content" in task_input or "file_path" in task_input

    def execute(self, task_input: Dict[str, Any], context_manager: ContextManager) -> DocumentAnalysisResult:
        start_time = time.time()
        self.status = AgentStatus.BUSY
        logger.info(f"{self.name} started execution.")
        
        try:
            content = task_input.get("document_content", "Mock document content loaded from file.")
            
            prompt = self.prompt_manager.load_prompt(
                "document_agent.md", 
                content=content,
                context=context_manager.get_context().model_dump_json()
            )
            
            llm = self.model_manager.get_active_model()
            result: DocumentAnalysisResult = llm.structured_invoke(
                prompt=prompt,
                schema=DocumentAnalysisResult
            )
            
            # Store in knowledge base
            self.knowledge_store.ingest_document(
                doc_id=f"doc_{int(time.time())}",
                content=content,
                source=task_input.get("file_path", "unknown"),
                doc_type="college_document"
            )
            
            self.confidence = result.confidence_score
            self.log_execution(start_time, task_input, result)
            return result
            
        except Exception as e:
            self.log_execution(start_time, task_input, None, error=e)
            raise

    def validate_output(self, output: Any) -> bool:
        return isinstance(output, DocumentAnalysisResult)
