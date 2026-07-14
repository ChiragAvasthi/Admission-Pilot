import logging
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.rag.chroma_store import ChromaVectorStore

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, vector_store: ChromaVectorStore):
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def process_and_store_document(self, doc_id: str, content: str, base_metadata: Dict[str, Any]) -> None:
        """
        Chunks the document and stores it in the vector database.
        """
        chunks = self.text_splitter.split_text(content)
        texts = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            texts.append(chunk)
            meta = base_metadata.copy()
            meta["chunk_index"] = i
            meta["doc_id"] = doc_id
            metadatas.append(meta)
            ids.append(f"{doc_id}_chunk_{i}")
            
        self.vector_store.add_documents(texts, metadatas, ids)
        logger.info(f"Document {doc_id} processed into {len(chunks)} chunks.")

    def retrieve_context(self, query: str, top_k: int = 3, filters: Dict[str, Any] = None) -> str:
        """
        Retrieves relevant context and formats it as a single string for LLM injection.
        """
        results = self.vector_store.search(query, top_k=top_k, filter_metadata=filters)
        
        context_parts = []
        for res in results:
            source = res['metadata'].get('source', 'Unknown')
            context_parts.append(f"--- SOURCE: {source} ---\n{res['content']}")
            
        return "\n\n".join(context_parts)
