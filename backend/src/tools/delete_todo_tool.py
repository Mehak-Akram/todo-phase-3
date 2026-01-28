import json
from typing import Dict, Any
from sqlmodel import Session
from datetime import datetime
import uuid

from ..models.todo import Todo
from ..database.database import engine
from ..services.todo_service import delete_todo as service_delete_todo


class DeleteTodoTool:
    @staticmethod
    def get_definition():
        """Return the function definition for OpenRouter function calling."""
        return {
            "name": "delete_todo",
            "description": "Delete an existing todo item for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo_id": {
                        "type": "string",
                        "description": "The ID of the todo to delete"
                    }
                },
                "required": ["todo_id"]
            }
        }

    async def execute(self, todo_id: str, user_id: str = None, db_session=None) -> Dict[str, Any]:
        """Execute the delete todo operation."""
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
                    raise ValueError("user_id is required to delete a todo")

                # Validate and convert user_id to UUID
                try:
                    user_uuid = uuid.UUID(user_id)
                except ValueError as e:
                    raise ValueError(f"Invalid user_id format: {user_id}. {str(e)}")

                # Validate and convert todo_id to UUID
                try:
                    todo_uuid = uuid.UUID(todo_id)
                except ValueError:
                    # If it's not a valid UUID, provide helpful guidance
                    return {
                        "success": False,
                        "error": f"Invalid todo ID format: {todo_id}. "
                                "Todo IDs are UUIDs (long alphanumeric strings). "
                                "To delete by content, say 'delete todo \"content\"'. "
                                "To delete by position, say 'delete todo at position 1'."
                    }

                success = service_delete_todo(
                    session=session,
                    todo_id=todo_uuid,
                    user_id=user_uuid
                )

                if not success:
                    return {
                        "success": False,
                        "error": f"Todo with ID {todo_id} not found or doesn't belong to user"
                    }

                return {
                    "success": True,
                    "message": f"Todo with ID {todo_id} deleted successfully",
                    "deleted_todo_id": todo_id
                }
            finally:
                # Only close the session if we created it
                if 'created_session' in locals() and created_session:
                    session.close()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete todo: {str(e)}"
            }