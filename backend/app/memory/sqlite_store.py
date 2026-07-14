import logging
import json
from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

Base = declarative_base()

class ConversationEntry(Base):
    __tablename__ = 'conversation_memory'
    id = Column(Integer, primary_key=True)
    session_id = Column(String, index=True)
    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class WorkspaceVariable(Base):
    __tablename__ = 'workspace_memory'
    id = Column(Integer, primary_key=True)
    workspace_id = Column(String, index=True)
    key = Column(String)
    value = Column(Text)  # JSON serialized

class SQLiteMemoryStore:
    """
    Persistent memory store utilizing SQLite for Conversation, Workspace, and Company memory.
    """
    def __init__(self, db_path: str = "sqlite:///memory.db"):
        self.engine = create_engine(db_path, connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_conversation_message(self, session_id: str, role: str, content: str) -> None:
        with self.Session() as session:
            entry = ConversationEntry(session_id=session_id, role=role, content=content)
            session.add(entry)
            session.commit()
            
    def get_conversation_history(self, session_id: str, limit: int = 50) -> List[Dict[str, str]]:
        with self.Session() as session:
            entries = session.query(ConversationEntry).filter_by(session_id=session_id).order_by(ConversationEntry.timestamp.desc()).limit(limit).all()
            return [{"role": e.role, "content": e.content} for e in reversed(entries)]

    def store_workspace_variable(self, workspace_id: str, key: str, value: Any) -> None:
        with self.Session() as session:
            existing = session.query(WorkspaceVariable).filter_by(workspace_id=workspace_id, key=key).first()
            json_val = json.dumps(value)
            if existing:
                existing.value = json_val
            else:
                new_var = WorkspaceVariable(workspace_id=workspace_id, key=key, value=json_val)
                session.add(new_var)
            session.commit()

    def get_workspace_variable(self, workspace_id: str, key: str) -> Optional[Any]:
        with self.Session() as session:
            var = session.query(WorkspaceVariable).filter_by(workspace_id=workspace_id, key=key).first()
            if var:
                return json.loads(var.value)
            return None
