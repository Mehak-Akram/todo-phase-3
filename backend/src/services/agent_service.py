import asyncio
import json
from typing import Dict, Any, List
from ..utils.openrouter_client import openrouter_client
from ..config import settings
from ..tools.create_todo_tool import CreateTodoTool
from ..tools.get_todos_tool import GetTodosTool
from ..tools.update_todo_tool import UpdateTodoTool
from ..tools.delete_todo_tool import DeleteTodoTool
from ..tools.set_todo_status_tool import SetTodoStatusTool
from ..tools.enhanced_todo_operations import DeleteTodoByContentTool, UpdateTodoByContentTool, DeleteTodoByPositionTool
from sqlalchemy.orm import Session
from ..database.database import get_session


class AgentService:
    def __init__(self):
        # Initialize tools that the agent can use
        self.tools = [
            {
                "type": "function",
                "function": CreateTodoTool.get_definition()
            },
            {
                "type": "function",
                "function": GetTodosTool.get_definition()
            },
            {
                "type": "function",
                "function": UpdateTodoTool.get_definition()
            },
            {
                "type": "function",
                "function": DeleteTodoTool.get_definition()
            },
            {
                "type": "function",
                "function": SetTodoStatusTool.get_definition()
            },
            {
                "type": "function",
                "function": DeleteTodoByContentTool.get_definition()
            },
            {
                "type": "function",
                "function": UpdateTodoByContentTool.get_definition()
            },
            {
                "type": "function",
                "function": DeleteTodoByPositionTool.get_definition()
            }
        ]

        # Map function names to actual tool instances
        self.tool_map = {
            "create_todo": CreateTodoTool(),
            "get_todos": GetTodosTool(),
            "update_todo": UpdateTodoTool(),
            "delete_todo": DeleteTodoTool(),
            "set_todo_status": SetTodoStatusTool(),
            "delete_todo_by_content": DeleteTodoByContentTool(),
            "update_todo_by_content": UpdateTodoByContentTool(),
            "delete_todo_by_position": DeleteTodoByPositionTool()
        }

    async def process_message(
        self,
        user_message: str,
        user_id: str,
        conversation_id: str,
        db_session=None  # Optional database session to ensure consistency
    ) -> Dict[str, Any]:
        """
        Process a user message with the AI agent.
        """
        try:
            # Prepare the conversation context
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful todo management assistant. "
                        "Help users manage their todos using natural language. "
                        "Parse user commands to extract todo content and intent. "
                        "For creation: When users say 'add todo', 'create todo', 'add task', 'create task', 'make todo', 'new todo', 'remind me to', or similar phrases, use the create_todo function. "
                        "Extract the main content from commands like 'add todo \"content\"' or 'create todo \"content\"'. "
                        "For deletion: if user specifies content, use delete_todo_by_content; if they specify position, use delete_todo_by_position; "
                        "if they use a command like 'delete todo \"content\" id: X', interpret this as wanting to delete by content, not by ID. "
                        "The ID field in user commands is often meant to indicate position (1-indexed), not the actual UUID. "
                        "Available functions: create_todo(title, description, due_date), get_todos(), update_todo(todo_id, content), delete_todo(todo_id), "
                        "delete_todo_by_content(content), delete_todo_by_position(position), update_todo_by_content(old_content, new_content). "
                        "Always respond in a friendly, conversational tone. "
                        "When a user asks to create a todo, be sure to call the create_todo function immediately."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]

            # Call OpenRouter API with function calling
            response = openrouter_client.chat.completions.create(
                model=settings.openrouter_model,  # Use the model from config
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                max_tokens=2048  # Limit tokens to avoid exceeding account limits
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Process any tool calls
            tool_results = []
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Add user_id to function args for proper authorization
                    # Ensure user_id is properly formatted as string
                    if isinstance(user_id, str):
                        function_args['user_id'] = user_id
                    elif hasattr(user_id, '__str__'):
                        function_args['user_id'] = str(user_id)
                    else:
                        function_args['user_id'] = str(user_id) if user_id else None

                    # Pass the database session if available to ensure consistency
                    if db_session is not None:
                        function_args['db_session'] = db_session

                    # Execute the tool
                    tool_instance = self.tool_map[function_name]
                    result = await tool_instance.execute(**function_args)

                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(result)
                    })

                # If there were tool calls, get the final response from the model
                if tool_results:
                    # Add tool results to messages
                    messages.extend([
                        response_message,
                        *tool_results
                    ])

                    # Get final response from model incorporating tool results
                    final_response = openrouter_client.chat.completions.create(
                        model=settings.openrouter_model,
                        messages=messages,
                        max_tokens=2048  # Limit tokens to avoid exceeding account limits
                    )
                    final_content = final_response.choices[0].message.content
                else:
                    final_content = response_message.content
            else:
                # No tool calls, just return the model's response
                final_content = response_message.content

            return {
                "response": final_content or "I processed your request successfully.",
                "tool_calls": [tc.model_dump() for tc in tool_calls] if tool_calls else [],
                "metadata": {
                    "user_message": user_message,
                    "processed_by": "agent_service"
                }
            }

        except Exception as e:
            return {
                "response": f"I encountered an error processing your request: {str(e)}. Could you please try again?",
                "tool_calls": [],
                "metadata": {
                    "error": str(e),
                    "user_message": user_message
                }
            }

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Return list of available tools for the agent.
        """
        return self.tools