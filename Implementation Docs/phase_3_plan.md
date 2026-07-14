# Admission Pilot - Phase 3 Implementation Plan
## AI Intelligence Layer

This document outlines the architecture and implementation strategy for the AI Intelligence Layer. This phase transforms the application into a true Agentic AI platform by implementing the core "brain" and intelligence infrastructure using LangGraph, Ollama, ChromaDB, and Pydantic-structured outputs.

### Dependencies
- **Added AI Libraries**: `langchain`, `langchain-community`, `langgraph`, `chromadb`, and `sentence-transformers` added to `pyproject.toml` and `requirements.txt`.

### Core LLM Integration
- `backend/app/llm/local_llm.py`: `LocalLLM` class handling Ollama connections, streaming, retries, and structured parsing via PydanticOutputParser.
- `backend/app/llm/model_manager.py`: `ModelManager` class for managing active models (Qwen3 default) and hot-swapping.

### Knowledge & RAG Pipeline
- `backend/app/embeddings/manager.py`: `EmbeddingManager` wrapping Sentence Transformers.
- `backend/app/rag/chroma_store.py`: ChromaDB integration for vector storage and semantic search.
- `backend/app/rag/pipeline.py`: Complete RAG framework (Loader, Chunker, Embedder, Retriever).
- `backend/app/knowledge/store.py`: Company Knowledge Base store for documents, reports, campaigns.

### Intelligence & Reasoning
- `backend/app/reasoning/engine.py`: `ReasoningEngine` to analyze goals, identify capabilities, and generate execution strategies.
- `backend/app/reflection/engine.py`: `ReflectionEngine` to evaluate outputs, detect hallucinations, and request regenerations.
- `backend/app/chains/context_builder.py`: `ContextBuilder` to fetch memory, RAG docs, and assemble optimal LLM context windows.

### Memory & State
- `backend/app/memory/sqlite_store.py`: SQLAlchemy models and store for persistent Conversation, Workspace, and Company Memory.
- `backend/app/parsers/structured.py`: Pydantic models for structured outputs (`ExecutionPlan`, `ReasoningResult`, `ReflectionResult`, `ToolCall`).

### Tools & Planning
- `backend/app/tools/base.py`: Generic `BaseTool` framework for future tools.
- `backend/app/agents/planner/planner.py`: Updated Planner to dynamically generate structured execution plans via LLM.

### Prompts
- `backend/app/agents/prompts/templates/`: Created specific Markdown templates for Planner, Reasoning, and Reflection prompts.

### Tests & Documentation
- `backend/tests/unit/ai/`: Unit tests covering LLM connection, memory retrieval, RAG, and Reflection.
- `docs/llm-architecture.md`: Markdown document explaining memory, prompt, RAG, and reasoning pipelines.
