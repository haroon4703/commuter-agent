from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum

class Status(str, Enum):
    SUCCESS = "success"
    ERROR = "error"

class AgentResponse(BaseModel):
    agent_name: str
    status: Status
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(BaseModel):
    role: Role
    content: str

class AgentRequest(BaseModel):
    messages: List[Message]
