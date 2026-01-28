from sqlmodel import create_engine, Session, SQLModel
from ..config import settings
import os

# Import models to ensure they're registered with SQLModel metadata
from ..models.todo import Todo
from ..models.conversation import Conversation, Message

# Use Neon PostgreSQL database exclusively
DATABASE_URL = settings.database_url

# Create engine with appropriate settings based on database type
if "sqlite" in DATABASE_URL.lower():
    # SQLite settings
    engine = create_engine(
        DATABASE_URL,
        echo=True
    )
else:
    # PostgreSQL/Neon settings with proper connection pooling
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,
        pool_recycle=300,
        # Additional settings for Neon compatibility
        connect_args={
            "sslmode": "require",
            "channel_binding": "require"
        }
    )

def create_db_and_tables():
    """Create database tables"""
    # For PostgreSQL, we need to handle schema updates manually
    # Create all tables that don't exist
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session