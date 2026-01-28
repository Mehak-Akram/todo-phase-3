import json
from typing import Dict, Any, Optional
from sqlmodel import Session
from datetime import datetime
import uuid

from ..models.todo import Todo, TodoUpdate
from ..database.database import engine
from ..services.todo_service import update_todo as service_update_todo


class UpdateTodoTool:
    @staticmethod
    def get_definition():
        """Return the function definition for OpenRouter function calling."""
        return {
            "name": "update_todo",
            "description": "Update an existing todo item for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo_id": {
                        "type": "string",
                        "description": "The ID of the todo to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title/content for the todo"
                    },
                    "content": {
                        "type": "string",
                        "description": "New content for the todo"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "Whether the todo is completed"
                    }
                },
                "required": ["todo_id"]
            }
        }

    async def execute(self, todo_id: str, title: Optional[str] = None,
                     content: Optional[str] = None, completed: Optional[bool] = None,
                     user_id: str = None, db_session=None) -> Dict[str, Any]:
        """Execute the update todo operation."""
        try:
            # Use the provided database session if available, otherwise create a new one
            if db_session:
                session = db_session
            else:
                session = Session(engine)
                # Track if we created the session to close it later
                created_session = True

            try:
                # Create update object using either title or content (title is treated as content)
                content_to_update = content or title
                todo_update = TodoUpdate(
                    content=content_to_update,
                    completed=completed
                )

                if not user_id:
                    raise ValueError("user_id is required to update a todo")

                # Validate and convert user_id and todo_id to UUID
                try:
                    user_uuid = uuid.UUID(user_id)
                    todo_uuid = uuid.UUID(todo_id)
                except ValueError as e:
                    raise ValueError(f"Invalid UUID format: user_id={user_id}, todo_id={todo_id}. {str(e)}")

                updated_todo = service_update_todo(
                    session=session,
                    todo_id=todo_uuid,
                    todo_update=todo_update,
                    user_id=user_uuid
                )

                if not updated_todo:
                    return {
                        "success": False,
                        "error": f"Todo with ID {todo_id} not found or doesn't belong to user"
                    }


                return {
                    "success": True,
                    "message": f"Todo '{updated_todo.content}' updated successfully",
                    "todo_id": str(updated_todo.id),
                    "content": updated_todo.content,
                    "completed": updated_todo.completed
                }
            finally:
                # Only close the session if we created it
                if 'created_session' in locals() and created_session:
                    session.close()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update todo: {str(e)}"
            }