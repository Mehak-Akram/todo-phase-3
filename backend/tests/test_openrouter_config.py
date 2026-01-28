"""
Test to verify OpenRouter configuration is properly set up.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_openrouter_config_exists():
    """Test that OpenRouter configuration exists in settings."""
    from src.config import settings

    # Check that OpenRouter settings exist
    assert hasattr(settings, 'openrouter_api_key'), "OpenRouter API key setting missing"
    assert hasattr(settings, 'openrouter_model'), "OpenRouter model setting missing"

    print("[PASS] OpenRouter settings exist in config")


def test_openrouter_client_can_be_imported():
    """Test that OpenRouter client can be imported without errors."""
    try:
        from src.utils.openrouter_client import openrouter_client
        print("[PASS] OpenRouter client can be imported")
    except ImportError as e:
        print(f"[FAIL] Failed to import OpenRouter client: {e}")
        raise


def test_no_openai_client_reference():
    """Test that old OpenAI client is no longer referenced."""
    import os

    # Check that openai_client.py file no longer exists
    openai_client_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'utils', 'openai_client.py')
    assert not os.path.exists(openai_client_path), "Old OpenAI client file still exists"

    print("[PASS] Old OpenAI client file has been removed")


def test_agent_service_uses_openrouter():
    """Test that agent service imports OpenRouter client."""
    # Read the agent service file to verify it imports openrouter_client
    agent_service_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'services', 'agent_service.py')

    with open(agent_service_path, 'r') as f:
        content = f.read()

    # Verify it imports openrouter_client
    assert 'openrouter_client' in content, "Agent service doesn't import openrouter_client"
    assert 'openai_client' not in content, "Agent service still references old openai_client"

    print("[PASS] Agent service uses OpenRouter client")


if __name__ == "__main__":
    print("Testing OpenRouter configuration...")

    test_openrouter_config_exists()
    test_openrouter_client_can_be_imported()
    test_no_openai_client_reference()
    test_agent_service_uses_openrouter()

    print("\nAll OpenRouter configuration tests passed!")