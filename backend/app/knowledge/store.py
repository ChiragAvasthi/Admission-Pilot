import logging
from typing import Dict, Any, List
from app.rag.pipeline import RAGPipeline
from app.rag.chroma_store import ChromaVectorStore

logger = logging.getLogger(__name__)

class KnowledgeStore:
    def __init__(self):
        self.vector_store = ChromaVectorStore(collection_name="company_knowledge")
        self.rag_pipeline = RAGPipeline(vector_store=self.vector_store)

    def ingest_document(self, doc_id: str, content: str, source: str, doc_type: str) -> None:
        """
        Ingest a document (report, campaign, web snapshot, etc.) into the knowledge base.
        """
        metadata = {
            "source": source,
            "type": doc_type
        }
        self.rag_pipeline.process_and_store_document(doc_id, content, metadata)
        logger.info(f"Ingested {doc_type} from {source}")

    def query_knowledge(self, query: str, doc_type: str = None) -> str:
        """
        Query the company knowledge base.
        """
        filters = {"type": doc_type} if doc_type else None
        return self.rag_pipeline.retrieve_context(query, filters=filters)
