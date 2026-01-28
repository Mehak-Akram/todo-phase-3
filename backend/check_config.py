import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

# Change to the src directory to resolve relative imports
original_cwd = os.getcwd()
os.chdir('src')

try:
    from config import settings
    print("Config loaded successfully")
    print(f"OpenRouter API key configured: {settings.openrouter_api_key != ''}")
    print(f"Database URL: {settings.database_url}")
    print(f"Debug mode: {settings.debug}")

    # Test OpenRouter client
    from utils.openrouter_client import get_openrouter_client
    print("\nTesting OpenRouter client...")
    try:
        client = get_openrouter_client()
        print("OpenRouter client created successfully!")
    except ValueError as e:
        print(f"OpenRouter client error: {e}")

    # Test agent service initialization
    from services.agent_service import AgentService
    print("\nTesting AgentService initialization...")
    agent_service = AgentService()
    print(f"AgentService initialized with {len(agent_service.tools)} tools")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Restore original working directory
    os.chdir(original_cwd)