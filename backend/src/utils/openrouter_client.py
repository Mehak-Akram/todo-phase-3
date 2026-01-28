from openai import OpenAI
from ..config import settings
import logging

logger = logging.getLogger(__name__)

def get_openrouter_client():
    """
    Initialize and return OpenRouter client with API key from settings
    Uses OpenAI-compatible API through OpenRouter
    """
    if not settings.openrouter_api_key:
        logger.error("OpenRouter API key is not configured. Please set OPENROUTER_API_KEY in your environment.")
        raise ValueError("OpenRouter API key is not configured")

    # Initialize OpenAI client with OpenRouter base URL
    client = OpenAI(
        api_key=settings.openrouter_api_key,
        base_url="https://openrouter.ai/api/v1"
    )
    return client

# Create a global client instance
openrouter_client = get_openrouter_client()