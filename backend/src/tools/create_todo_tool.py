import json
from typing import Dict, Any, Optional
from sqlmodel import Session
from datetime import datetime
import uuid
import logging

from ..models.todo import Todo, TodoCreate
from ..database.database import engine
from ..services.todo_service import create_todo as service_create_todo


class CreateTodoTool:
    @staticmethod
    def get_definition():
        """Return the function definition for OpenRouter function calling."""
        return {
            "name": "create_todo",
            "description": "Create a new todo item for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title or content of the todo item"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional detailed description of the todo"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Optional due date in YYYY-MM-DD format"
                    }
                },
                "required": ["title"]
            }
        }

    async def execute(self, title: str, description: Optional[str] = None,
                     due_date: Optional[str] = None, user_id: str = None,
                     db_session=None) -> Dict[str, Any]:
        """Execute the create todo operation."""
        try:
            # Combine title and description if both are provided
            combined_title = title
            if description and description.lower() not in ['none', 'null', '', 'undefined']:
                # Check if description is already contained in title or vice versa
                if description.lower() not in title.lower() and title.lower() not in description.lower():
                    combined_title = f"{title}: {description}"

            # Parse due_date if provided
            parsed_due_date = None
            if due_date and due_date.lower() not in ['none', 'null', '', 'undefined']:
                from datetime import datetime
                try:
                    parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    # If the format is wrong, try other common formats
                    try:
                        parsed_due_date = datetime.strptime(due_date, "%Y-%m-%dT%H:%M:%S")
                    except ValueError:
                        # If still wrong, log but continue without due date
                        logging.warning(f"Invalid due date format: {due_date}")

            # Create TodoCreate object
            todo_create = TodoCreate(
                content=combined_title,  # Using content field to match existing Todo model
                completed=False,
                due_date=parsed_due_date
                # source field has been temporarily removed due to schema mismatch
            )

            if not user_id:
                raise ValueError("user_id is required to create a todo")

            # Validate and convert user_id to UUID
            try:
                user_uuid = uuid.UUID(user_id)
            except ValueError:
                # Try to handle common UUID format issues
                if isinstance(user_id, str) and len(user_id) == 36 and user_id.count('-') == 4:
                    # Already in proper format
                    user_uuid = uuid.UUID(user_id)
                else:
                    raise ValueError(f"Invalid user_id format: {user_id}. Expected a valid UUID.")

            # Use the provided database session if available, otherwise create a new one
            if db_session:
                # Use the provided session to ensure consistency with the calling context
                new_todo = service_create_todo(
                    session=db_session,
                    todo_create=todo_create,
                    user_id=user_uuid
                )

                # Note: Don't commit here as the main request flow handles the commit
            else:
                # Fallback to creating a new session if none provided
                # This maintains backward compatibility
                with Session(engine) as session:
                    new_todo = service_create_todo(
                        session=session,
                        todo_create=todo_create,
                        user_id=user_uuid
                    )

            return {
                "success": True,
                "message": f"Todo '{combined_title}' created successfully",
                "todo_id": str(new_todo.id),
                "content": new_todo.content,
                "completed": new_todo.completed,
                "due_date": str(new_todo.due_date) if new_todo.due_date else None
                # source field has been temporarily removed due to schema mismatch
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create todo: {str(e)}"
            }