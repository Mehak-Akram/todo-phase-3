from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..models.user import User

def get_todos_by_user(session: Session, user_id: UUID) -> List[Todo]:
    """Get all todos for a specific user"""
    statement = select(Todo).where(Todo.user_id == user_id)
    todos = session.exec(statement).all()
    return todos

def get_todo_by_id(session: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
    """Get a specific todo by ID for a specific user"""
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.exec(statement).first()
    return todo

def create_todo(session: Session, todo_create: TodoCreate, user_id: UUID) -> Todo:
    """Create a new todo for a user"""
    db_todo = Todo(
        content=todo_create.content,
        completed=todo_create.completed,
        due_date=todo_create.due_date,
        user_id=user_id
        # source is temporarily omitted due to schema mismatch
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo

def update_todo(session: Session, todo_id: UUID, todo_update: TodoUpdate, user_id: UUID) -> Optional[Todo]:
    """Update a specific todo for a user"""
    db_todo = get_todo_by_id(session, todo_id, user_id)
    if not db_todo:
        return None

    # Update fields if provided
    if todo_update.content is not None:
        db_todo.content = todo_update.content
    if todo_update.completed is not None:
        db_todo.completed = todo_update.completed
    if todo_update.due_date is not None:
        db_todo.due_date = todo_update.due_date

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def delete_todo(session: Session, todo_id: UUID, user_id: UUID) -> bool:
    """Delete a specific todo for a user"""
    db_todo = get_todo_by_id(session, todo_id, user_id)
    if not db_todo:
        return False

    session.delete(db_todo)
    session.commit()
    return True

def toggle_todo_completion(session: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
    """Toggle completion status of a specific todo for a user"""
    db_todo = get_todo_by_id(session, todo_id, user_id)
    if not db_todo:
        return None

    db_todo.completed = not db_todo.completed
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo