#!/usr/bin/env python3
"""
Simple test to verify OpenRouter API connection.
"""

import os
import sys
from openai import OpenAI

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import settings

def test_api_connection():
    """Test basic API connection."""
    print("Testing OpenRouter API connection...")
    print(f"Model: {settings.openrouter_model}")
    print(f"API Key configured: {bool(settings.openrouter_api_key)}")

    if not settings.openrouter_api_key:
        print("❌ ERROR: No OpenRouter API key found in settings")
        return False

    try:
        # Initialize OpenAI client with OpenRouter base URL
        client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        # Make a simple test call
        response = client.chat.completions.create(
            model=settings.openrouter_model,
            messages=[
                {"role": "user", "content": "Hello, this is a test message to check if the API is working. Just respond with 'API is working'."}
            ],
            max_tokens=100
        )

        print(f"[SUCCESS] API responded with: {response.choices[0].message.content}")
        return True

    except Exception as e:
        print(f"[ERROR] API call failed with error: {e}")
        return False

if __name__ == "__main__":
    test_api_connection()