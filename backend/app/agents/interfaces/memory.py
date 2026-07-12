from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class ConversationMemory(ABC):
    @abstractmethod
    def add_message(self, role: str, content: str) -> None:
        pass

    @abstractmethod
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

class VectorMemory(ABC):
    @abstractmethod
    def store_document(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        pass

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        pass

class WorkspaceMemory(ABC):
    @abstractmethod
    def store_variable(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def get_variable(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def list_variables(self) -> Dict[str, Any]:
        pass
