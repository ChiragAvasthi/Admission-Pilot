from enum import Enum, auto

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class AgentStatus(str, Enum):
    IDLE = "IDLE"
    BUSY = "BUSY"
    ERROR = "ERROR"
    OFFLINE = "OFFLINE"

class WorkflowStatus(str, Enum):
    INITIALIZED = "INITIALIZED"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    REVIEWING = "REVIEWING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"

class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Capability(str, Enum):
    PLANNING = "PLANNING"
    RESEARCH = "RESEARCH"
    CODING = "CODING"
    REVIEW = "REVIEW"
    WRITING = "WRITING"
    ORCHESTRATION = "ORCHESTRATION"
