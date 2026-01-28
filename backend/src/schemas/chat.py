from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    metadata: Optional[dict] = {}


class ChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    response: str
    timestamp: datetime
    tool_calls: List[dict] = []
    error: Optional[str] = None


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    timestamp: datetime
    metadata: Optional[dict] = {}


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    is_active: bool