#!/usr/bin/env python3
"""
Test script to verify that the token limits are properly set in OpenRouter API calls.
"""

import asyncio
import sys
import os
from unittest.mock import Mock, patch

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.agent_service import AgentService
from utils.openrouter_client import openrouter_client
from config import settings

async def test_token_limits():
    """Test that the agent service makes API calls with token limits."""
    print("Testing token limits in Agent Service...")

    # Create mock response
    mock_completion = Mock()
    mock_message = Mock()
    mock_message.tool_calls = None
    mock_message.content = "This is a test response from the AI."
    mock_choice = Mock()
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]

    # Track if the API was called with max_tokens
    call_kwargs = {}

    def mock_create(*args, **kwargs):
        call_kwargs.update(kwargs)
        return mock_completion

    # Replace the actual client with a mock that tracks calls
    original_create = openrouter_client.chat.completions.create
    openrouter_client.chat.completions.create = mock_create

    try:
        # Initialize the agent service
        agent_service = AgentService()

        # Call the process_message method
        result = await agent_service.process_message(
            user_message="Hello, how are you?",
            user_id="test_user_id",
            conversation_id="test_conversation_id"
        )

        # Check if max_tokens was passed to the API call
        if 'max_tokens' in call_kwargs:
            print(f"✅ SUCCESS: max_tokens was set to {call_kwargs['max_tokens']}")
        else:
            print("❌ FAILED: max_tokens was not set in the API call")

        print(f"Response: {result['response']}")
        print("✅ Token limit test completed successfully!")

    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Restore the original client
        openrouter_client.chat.completions.create = original_create

if __name__ == "__main__":
    print("Starting token limit verification test...")
    print(f"OpenRouter model: {settings.openrouter_model}")
    print(f"OpenRouter API key configured: {bool(settings.openrouter_api_key)}")

    asyncio.run(test_token_limits())