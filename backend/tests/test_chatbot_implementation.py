"""
Basic tests to verify the AI Chatbot for Todo Management implementation.
These tests verify that the core components are properly connected.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

from src.services.agent_service import AgentService
from src.services.chat_service import ChatService
from src.tools.create_todo_tool import CreateTodoTool
from src.tools.get_todos_tool import GetTodosTool
from src.tools.update_todo_tool import UpdateTodoTool
from src.tools.delete_todo_tool import DeleteTodoTool
from src.tools.set_todo_status_tool import SetTodoStatusTool


def test_create_todo_tool_exists():
    """Test that the CreateTodo tool is properly defined."""
    tool = CreateTodoTool()
    definition = tool.get_definition()

    assert definition["name"] == "create_todo"
    assert "description" in definition
    assert "parameters" in definition
    assert callable(tool.execute)


def test_get_todos_tool_exists():
    """Test that the GetTodos tool is properly defined."""
    tool = GetTodosTool()
    definition = tool.get_definition()

    assert definition["name"] == "get_todos"
    assert "description" in definition
    assert "parameters" in definition
    assert callable(tool.execute)


def test_update_todo_tool_exists():
    """Test that the UpdateTodo tool is properly defined."""
    tool = UpdateTodoTool()
    definition = tool.get_definition()

    assert definition["name"] == "update_todo"
    assert "description" in definition
    assert "parameters" in definition
    assert callable(tool.execute)


def test_delete_todo_tool_exists():
    """Test that the DeleteTodo tool is properly defined."""
    tool = DeleteTodoTool()
    definition = tool.get_definition()

    assert definition["name"] == "delete_todo"
    assert "description" in definition
    assert "parameters" in definition
    assert callable(tool.execute)


def test_set_todo_status_tool_exists():
    """Test that the SetTodoStatus tool is properly defined."""
    tool = SetTodoStatusTool()
    definition = tool.get_definition()

    assert definition["name"] == "set_todo_status"
    assert "description" in definition
    assert "parameters" in definition
    assert callable(tool.execute)


def test_agent_service_initialization():
    """Test that the AgentService initializes properly."""
    agent_service = AgentService()

    assert hasattr(agent_service, 'tools')
    assert len(agent_service.tools) == 5  # All 5 tools should be registered
    assert hasattr(agent_service, 'tool_map')
    assert len(agent_service.tool_map) == 5  # All 5 tools should be mapped


def test_tool_mapping_consistency():
    """Test that tool definitions match the mapping in AgentService."""
    agent_service = AgentService()

    # Get tool names from definitions
    tool_names_from_definitions = {tool['function']['name'] for tool in agent_service.tools}

    # Get tool names from mapping
    tool_names_from_mapping = set(agent_service.tool_map.keys())

    # Both should match
    assert tool_names_from_definitions == tool_names_from_mapping
    assert len(tool_names_from_definitions) == 5


if __name__ == "__main__":
    # Run the tests
    test_create_todo_tool_exists()
    test_get_todos_tool_exists()
    test_update_todo_tool_exists()
    test_delete_todo_tool_exists()
    test_set_todo_status_tool_exists()
    test_agent_service_initialization()
    test_tool_mapping_consistency()

    print("All tests passed! AI Chatbot implementation is correctly set up.")