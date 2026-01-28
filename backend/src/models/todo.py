from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum
from .user import User

class SourceType(str, Enum):
    manual = "manual"
    chatbot = "chatbot"

class TodoBase(SQLModel):
    content: str
    completed: bool = False
    user_id: uuid.UUID = Field(foreign_key="user.id")

class Todo(TodoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str = Field(nullable=False)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = Field(default=None)  # Added due_date field
    # source: Optional[SourceType] = Field(default=SourceType.manual)  # Temporarily removed due to schema mismatch

    # Relationship to user
    user: User = Relationship(back_populates="todos")

class TodoCreate(SQLModel):
    content: str
    completed: bool = False
    due_date: Optional[datetime] = None
    # source: Optional[SourceType] = SourceType.manual  # Temporarily removed due to schema mismatch

class TodoRead(TodoBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    # source: Optional[SourceType]  # Temporarily removed due to schema mismatch

class TodoUpdate(SQLModel):
    content: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None