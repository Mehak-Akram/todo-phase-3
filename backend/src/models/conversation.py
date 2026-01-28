from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import JSON
from sqlalchemy.types import JSON as SQLJSON

if TYPE_CHECKING:
    from .todo import Todo  # Import for type checking to avoid circular imports


class RoleType(str, Enum):
    user = "user"
    assistant = "assistant"


class SourceType(str, Enum):
    manual = "manual"
    chatbot = "chatbot"


class Conversation(SQLModel, table=True):
    """
    Represents a user's chat session with the AI assistant.
    """
    __tablename__ = "conversation"  # Explicitly set table name

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(index=True)  # Foreign Key to users table
    thread_id: Optional[str] = Field(default=None, max_length=255)  # Thread ID for the conversation (optional)
    title: str = Field(max_length=255)
    created_at: datetime = Field(default=datetime.utcnow)
    updated_at: datetime = Field(default=datetime.utcnow)

    # Relationship to messages in this conversation
    messages: list["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """
    Represents an individual chat message within a conversation.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)
    role: RoleType = Field(sa_column="role")
    content: str = Field(max_length=10000)
    timestamp: datetime = Field(default=datetime.utcnow)

    # Relationship to the conversation this message belongs to
    conversation: Conversation = Relationship(back_populates="messages")