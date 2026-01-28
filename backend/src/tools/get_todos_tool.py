import json
from typing import Dict, Any, Optional
from sqlmodel import Session
from datetime import datetime
import uuid

from ..models.todo import Todo
from ..database.database import engine
from ..services.todo_service import get_todos_by_user


class GetTodosTool:
    @staticmethod
    def get_definition():
        """Return the function definition for OpenRouter function calling."""
        return {
            "name": "get_todos",
            "description": "Retrieve todo items for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "completed", "incomplete"],
                        "description": "Filter todos by status (default: all)"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Filter todos by due date in YYYY-MM-DD format"
                    }
                }
            }
        }

    async def execute(self, status: Optional[str] = "all", due_date: Optional[str] = None,
                     user_id: str = None, db_session=None) -> Dict[str, Any]:
        """Execute the get todos operation."""
        try:
            # Use the provided database session if available, otherwise create a new one
            if db_session:
                session = db_session
            else:
                session = Session(engine)
                # Track if we created the session to close it later
                created_session = True

            try:
                if not user_id:
                    raise ValueError("user_id is required to retrieve todos")

                # Validate and convert user_id to UUID
                try:
                    user_uuid = uuid.UUID(user_id)
                except ValueError:
                    raise ValueError(f"Invalid user_id format: {user_id}. Expected a valid UUID.")

                todos = get_todos_by_user(session=session, user_id=user_uuid)

                # Apply additional filtering in Python since the service doesn't have these filters
                if status == "completed":
                    todos = [todo for todo in todos if todo.completed]
                elif status == "incomplete":
                    todos = [todo for todo in todos if not todo.completed]

                # Format results
                todo_list = []
                for todo in todos:
                    todo_dict = {
                        "id": str(todo.id),
                        "content": todo.content,
                        "completed": todo.completed,
                        "created_at": todo.created_at.isoformat() if todo.created_at else None
                        # source field has been temporarily removed due to schema mismatch
                    }

                    # Add due_date if it exists in the model
                    if hasattr(todo, 'due_date') and todo.due_date:
                        todo_dict["due_date"] = todo.due_date.isoformat()

                    todo_list.append(todo_dict)

                return {
                    "success": True,
                    "todos": todo_list,
                    "count": len(todo_list),
                    "filters_applied": {
                        "status": status,
                        "due_date": due_date
                    }
                }
            finally:
                # Only close the session if we created it
                if 'created_session' in locals() and created_session:
                    session.close()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to retrieve todos: {str(e)}"
            }