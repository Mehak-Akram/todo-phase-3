from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate
from ..utils.password_utils import get_password_hash
from ..utils.db_utils import get_user_by_email

import uuid

def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    """Get a user by ID"""
    try:
        # Convert string to UUID for comparison with database field
        user_uuid = uuid.UUID(user_id)
        statement = select(User).where(User.id == user_uuid)
        user = session.exec(statement).first()
        return user
    except ValueError:
        # If user_id is not a valid UUID, return None
        return None

def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        email=user_create.email,
        password_hash=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def update_user(session: Session, user_id: str, user_update) -> Optional[User]:
    """Update a user"""
    try:
        user_uuid = uuid.UUID(user_id)
        db_user = get_user_by_id(session, user_id)  # get_user_by_id handles the conversion
        if not db_user:
            return None

        # Update fields if provided
        if user_update.email:
            db_user.email = user_update.email
        if user_update.password:
            db_user.password_hash = get_password_hash(user_update.password)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except ValueError:
        return None

def delete_user(session: Session, user_id: str) -> bool:
    """Delete a user"""
    try:
        db_user = get_user_by_id(session, user_id)  # get_user_by_id handles the conversion
        if not db_user:
            return False

        session.delete(db_user)
        session.commit()
        return True
    except ValueError:
        return False