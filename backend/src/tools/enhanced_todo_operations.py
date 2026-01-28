"""
Enhanced todo operations that can handle content-based lookups.
"""
import json
from typing import Dict, Any, Optional
from sqlmodel import Session
from datetime import datetime
import uuid

from ..models.todo import Todo, TodoUpdate
from ..database.database import engine
from ..services.todo_service import (
    get_todos_by_user,
    delete_todo as service_delete_todo,
    update_todo as service_update_todo,
    create_todo as service_create_todo
)
from .get_todos_tool import GetTodosTool


class EnhancedTodoOperations:
    """Class containing enhanced operations that can handle content-based lookups."""

    @staticmethod
    def find_todo_by_content(session: Session, user_id: uuid.UUID, content: str) -> Optional[Todo]:
        """
        Find a todo by its content.
        """
        todos = get_todos_by_user(session=session, user_id=user_id)

        # Exact match first
        for todo in todos:
            if todo.content.lower().strip() == content.lower().strip():
                return todo

        # Partial match as fallback
        for todo in todos:
            if content.lower().strip() in todo.content.lower():
                return todo

        return None

    @staticmethod
    def find_todo_by_partial_match(session: Session, user_id: uuid.UUID, search_term: str) -> Optional[Todo]:
        """
        Find a todo by partial matching of content.
        """
        todos = get_todos_by_user(session=session, user_id=user_id)

        # Look for partial matches
        for todo in todos:
            if search_term.lower() in todo.content.lower():
                return todo

        return None


class DeleteTodoByContentTool:
    """Tool to delete a todo by content instead of ID."""

    @staticmethod
    def get_definition():
        """Return the function definition for OpenRouter function calling."""
        return {
            "name": "delete_todo_by_content",
            "description": "Delete a todo by its content/title instead of ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content/title of the todo to delete"
                    }
                },
                "required": ["content"]
            }
        }

    async def execute(self, content: str, user_id: str = None, db_session=None) -> Dict[str, Any]:
        """Execute the delete todo by content operation."""
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
                except ValueError:
                    raise ValueError(f"Invalid user_id format: {user_id}. Expected a valid UUID.")

                # Find the todo by content
                todo = EnhancedTodoOperations.find_todo_by_content(
                    session=session,
                    user_id=user_uuid,
                    content=content
                )

                if not todo:
                    # Get all todos to provide helpful suggestions
                    all_todos = get_todos_by_user(session=session, user_id=user_uuid)
                    todo_contents = [t.content for t in all_todos]

                    # Provide suggestions for similar content if available
                    suggestions = []
                    content_lower = content.lower().strip()
                    for todo_content in todo_contents:
                        if content_lower in todo_content.lower() or todo_content.lower() in content_lower:
                            suggestions.append(todo_content)

                    error_msg = f"No exact match found for todo with content '{content}'."
                    if suggestions:
                        error_msg += f" Did you mean: {', '.join(suggestions[:3])}?"
                    elif todo_contents:
                        error_msg += f" Available todos: {', '.join(todo_contents[:5])}..."

                    return {
                        "success": False,
                        "error": error_msg,
                        "available_todos": todo_contents
                    }

                # Delete the found todo
                success = service_delete_todo(
                    session=session,
                    todo_id=todo.id,
                    user_id=user_uuid
                )

                if not success:
                    return {
                        "success": False,
                        "error": f"Failed to delete todo with content '{content}'"
                    }

                return {
                    "success": True,
                    "message": f"Todo '{content}' deleted successfully",
                    "deleted_todo_id": str(todo.id),
                    "deleted_content": content
                }
            finally:
                # Only close the session if we created it
                if 'created_session' in locals() and created_session:
                    session.close()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete todo by content: {str(e)}"
            }


class UpdateTodoByContentTool:
    """Tool to update a todo by content instead of ID."""

    @staticmethod
    def get_definition():
        """Return the function definition for OpenRouter function calling."""
        return {
            "name": "update_todo_by_content",
            "description": "Update a todo by its content/title instead of ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "old_content": {
                        "type": "string",
                        "description": "The current content/title of the todo to update"
                    },
                    "new_content": {
                        "type": "string",
                        "description": "The new content for the todo"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "Whether the todo is completed"
                    }
                },
                "required": ["old_content"]
            }
        }

    async def execute(self, old_content: str, new_content: Optional[str] = None,
                     completed: Optional[bool] = None, user_id: str = None,
                     db_session=None) -> Dict[str, Any]:
        """Execute the update todo by content operation."""
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
                    raise ValueError("user_id is required to update a todo")

                # Validate and convert user_id to UUID
                try:
                    user_uuid = uuid.UUID(user_id)
                except ValueError:
                    raise ValueError(f"Invalid user_id format: {user_id}. Expected a valid UUID.")

                # Find the todo by content
                todo = EnhancedTodoOperations.find_todo_by_content(
                    session=session,
                    user_id=user_uuid,
                    content=old_content
                )

                if not todo:
                    # Get all todos to provide helpful suggestions
                    all_todos = get_todos_by_user(session=session, user_id=user_uuid)
                    todo_contents = [t.content for t in all_todos]

                    # Provide suggestions for similar content if available
                    suggestions = []
                    content_lower = old_content.lower().strip()
                    for todo_content in todo_contents:
                        if content_lower in todo_content.lower() or todo_content.lower() in content_lower:
                            suggestions.append(todo_content)

                    error_msg = f"No exact match found for todo with content '{old_content}'."
                    if suggestions:
                        error_msg += f" Did you mean: {', '.join(suggestions[:3])}?"
                    elif todo_contents:
                        error_msg += f" Available todos: {', '.join(todo_contents[:5])}..."

                    return {
                        "success": False,
                        "error": error_msg,
                        "available_todos": todo_contents
                    }

                # Prepare update object
                todo_update = TodoUpdate()
                if new_content is not None:
                    todo_update.content = new_content
                else:
                    todo_update.content = todo.content  # Keep existing content if not specified
                if completed is not None:
                    todo_update.completed = completed
                else:
                    todo_update.completed = todo.completed  # Keep existing status if not specified

                # Update the found todo
                updated_todo = service_update_todo(
                    session=session,
                    todo_id=todo.id,
                    todo_update=todo_update,
                    user_id=user_uuid
                )

                if not updated_todo:
                    return {
                        "success": False,
                        "error": f"Failed to update todo with content '{old_content}'"
                    }

                return {
                    "success": True,
                    "message": f"Todo '{old_content}' updated successfully",
                    "todo_id": str(updated_todo.id),
                    "old_content": old_content,
                    "new_content": updated_todo.content,
                    "completed": updated_todo.completed
                }
            finally:
                # Only close the session if we created it
                if 'created_session' in locals() and created_session:
                    session.close()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update todo by content: {str(e)}"
            }


class DeleteTodoByPositionTool:
    """Tool to delete a todo by its position in the list (1-indexed)."""

    @staticmethod
    def get_definition():
        """Return the function definition for OpenRouter function calling."""
        return {
            "name": "delete_todo_by_position",
            "description": "Delete a todo by its position in the list (1-indexed)",
            "parameters": {
                "type": "object",
                "properties": {
                    "position": {
                        "type": "integer",
                        "description": "The position of the todo in the list (1 for first, 2 for second, etc.)"
                    }
                },
                "required": ["position"]
            }
        }

    async def execute(self, position: int, user_id: str = None, db_session=None) -> Dict[str, Any]:
        """Execute the delete todo by position operation."""
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
                except ValueError:
                    raise ValueError(f"Invalid user_id format: {user_id}. Expected a valid UUID.")

                # Get all todos for the user
                todos = get_todos_by_user(session=session, user_id=user_uuid)

                # Check if position is valid
                if position < 1 or position > len(todos):
                    # Format available todos with positions for helpful feedback
                    available_todos_formatted = [
                        {"position": i+1, "content": t.content, "id": str(t.id)[:8] + "..."}
                        for i, t in enumerate(todos)
                    ] if todos else []

                    error_msg = f"Position {position} is out of range. You have {len(todos)} todos. "
                    if todos:
                        error_msg += "Available positions: "
                        error_msg += ", ".join([f"'{i+1}' for '{t.content}'" for i, t in enumerate(todos[:5])])  # Show first 5
                        if len(todos) > 5:
                            error_msg += f" and {len(todos)-5} more..."
                    else:
                        error_msg += "No todos available."

                    return {
                        "success": False,
                        "error": error_msg,
                        "available_todos": available_todos_formatted
                    }

                # Get the todo at the specified position (1-indexed)
                todo_to_delete = todos[position - 1]

                # Delete the todo
                success = service_delete_todo(
                    session=session,
                    todo_id=todo_to_delete.id,
                    user_id=user_uuid
                )

                if not success:
                    return {
                        "success": False,
                        "error": f"Failed to delete todo at position {position}"
                    }

                return {
                    "success": True,
                    "message": f"Todo at position {position} ('{todo_to_delete.content}') deleted successfully",
                    "deleted_todo_id": str(todo_to_delete.id),
                    "deleted_content": todo_to_delete.content,
                    "position": position
                }
            finally:
                # Only close the session if we created it
                if 'created_session' in locals() and created_session:
                    session.close()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete todo by position: {str(e)}"
            }