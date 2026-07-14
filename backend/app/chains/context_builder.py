import logging
from typing import Dict, Any, Optional
from app.memory.sqlite_store import SQLiteMemoryStore
from app.knowledge.store import KnowledgeStore
from app.agents.state.context import ContextManager

logger = logging.getLogger(__name__)

class ContextBuilder:
    """
    Assembles memory, retrieved knowledge, and active context variables into
    a single prompt-ready string for the LLM.
    """
    def __init__(self, memory_store: SQLiteMemoryStore, knowledge_store: KnowledgeStore):
        self.memory_store = memory_store
        self.knowledge_store = knowledge_store

    def build_context(self, session_id: str, query: str, context_manager: ContextManager) -> str:
        # 1. Fetch Conversation History
        history = self.memory_store.get_conversation_history(session_id, limit=5)
        history_str = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])
        
        # 2. Fetch RAG Knowledge
        knowledge_str = self.knowledge_store.query_knowledge(query)
        
        # 3. Active Agent Context
        active_context = context_manager.get_context()
        active_ctx_str = (
            f"Goal: {active_context.goal}\n"
            f"Company: {active_context.company or 'Unknown'}\n"
            f"Extracted Info: {active_context.extracted_information}\n"
        )
        
        # Assemble
        assembled = (
            "--- ACTIVE CONTEXT ---\n"
            f"{active_ctx_str}\n\n"
            "--- RELEVANT KNOWLEDGE ---\n"
            f"{knowledge_str if knowledge_str else 'No relevant knowledge found.'}\n\n"
            "--- RECENT CONVERSATION ---\n"
            f"{history_str if history_str else 'No prior conversation.'}\n"
        )
        
        return assembled
