import logging
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from app.embeddings.manager import EmbeddingManager

logger = logging.getLogger(__name__)

class ChromaVectorStore:
    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "company_knowledge"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedding_manager = EmbeddingManager()
        logger.info(f"ChromaDB initialized at {persist_directory} with collection {collection_name}")

    def add_documents(self, texts: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> None:
        if not texts:
            return
        embeddings = self.embedding_manager.embed_batch(texts)
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Added {len(texts)} documents to ChromaDB.")

    def search(self, query: str, top_k: int = 5, filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        query_embedding = self.embedding_manager.embed_text(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata
        )
        
        parsed_results = []
        if results['documents'] and len(results['documents']) > 0:
            for doc, meta, id, dist in zip(results['documents'][0], results['metadatas'][0], results['ids'][0], results['distances'][0]):
                parsed_results.append({
                    "id": id,
                    "content": doc,
                    "metadata": meta,
                    "distance": dist
                })
        return parsed_results
