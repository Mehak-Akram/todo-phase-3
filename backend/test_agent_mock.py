import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

# Add the project root to the path so relative imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
print("Config loaded successfully")
print(f"OpenRouter API key configured: {settings.openrouter_api_key != ''}")
print(f"Database URL: {settings.database_url}")
print(f"Debug mode: {settings.debug}")

# Test agent service initialization by directly importing and mocking the problematic parts
import importlib.util
from unittest.mock import Mock, patch

# Try to test the agent service with mocked OpenRouter client
print("\nTesting AgentService initialization with mocked client...")

# Create a mock for openrouter_client
mock_openrouter_client = Mock()
mock_completion = Mock()
mock_message = Mock()
mock_message.tool_calls = None
mock_message.content = "Test response"
mock_choice = Mock()
mock_choice.message = mock_message
mock_completion.choices = [mock_choice]

mock_openrouter_client.chat.completions.create.return_value = mock_completion

# Patch the import
with patch.dict('sys.modules', {'..utils.openrouter_client': Mock(openrouter_client=mock_openrouter_client)}):
    # Need to temporarily modify sys.modules to handle the relative import
    import sys
    from unittest.mock import MagicMock

    # Create a mock for the module
    mock_config = MagicMock()
    mock_config.settings = settings

    # Add to sys.modules to avoid the relative import issue
    sys.modules['..config'] = mock_config
    sys.modules['src.config'] = mock_config
    sys.modules['..database.database'] = MagicMock()

    # Now try to import the agent service
    try:
        # Temporarily add the src directory to the path
        original_modules = dict(sys.modules)

        # Reload the modules with proper path
        import importlib

        # Add the necessary modules
        sys.modules['..utils.openrouter_client'] = Mock(openrouter_client=mock_openrouter_client)
        sys.modules['..config'] = Mock(settings=settings)
        sys.modules['..database.database'] = Mock()

        # Import with modified sys.modules
        from services.agent_service import AgentService
        print("AgentService imported successfully")

        # Test initialization
        agent_service = AgentService()
        print(f"AgentService initialized with {len(agent_service.tools)} tools")

        # Test the process_message method with mocked dependencies
        import asyncio

        async def test_process_message():
            result = await agent_service.process_message("Test message", "test_user_id", "test_conv_id")
            print(f"Process message result keys: {list(result.keys())}")
            print(f"Response: {result.get('response', 'No response')}")

        # Run the async test
        asyncio.run(test_process_message())

    except Exception as e:
        print(f"Error with AgentService: {e}")
        import traceback
        traceback.print_exc()