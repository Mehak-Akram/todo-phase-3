#!/usr/bin/env python3
"""
Test the chat API endpoint directly to troubleshoot the "chatbot is not answering" issue.
"""

import requests
import json

# Test the backend API directly
BASE_URL = "http://localhost:8000"

def test_health():
    """Test if backend is running."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Backend health: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Backend health check failed: {e}")
        return False

def test_chat_api():
    """Test the chat API endpoint."""
    # First, we need to authenticate or get a valid token
    # For now, let's check if the route exists
    try:
        # Try to access the chat endpoint without authentication to see the error
        headers = {
            'Content-Type': 'application/json',
        }

        payload = {
            "message": "Hello, can you help me create a todo?",
            "conversation_id": None
        }

        response = requests.post(f"{BASE_URL}/api/v1/chat/",
                                headers=headers,
                                data=json.dumps(payload))

        print(f"Chat API response: {response.status_code}")
        print(f"Chat API response body: {response.text}")

        # The 401 Unauthorized error is expected since we're not authenticated
        if response.status_code == 401:
            print("Got expected 401 Unauthorized - need to authenticate first")
            return True
        elif response.status_code == 200:
            print("Chat API working properly!")
            return True
        else:
            print(f"Unexpected response: {response.status_code}")
            return False

    except Exception as e:
        print(f"Chat API test failed: {e}")
        return False

def test_auth_required():
    """Test authentication endpoints."""
    try:
        # Try to register a test user or login
        response = requests.get(f"{BASE_URL}/api/auth/me")
        print(f"Auth check response: {response.status_code}")

        if response.status_code == 401:
            print("Authentication required - this is expected")
            return True
        else:
            print(f"Auth check unexpected response: {response.status_code}")
            return True  # Not necessarily an error

    except Exception as e:
        print(f"Auth test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend API connectivity...")

    if test_health():
        print("\nHealth check passed!")
    else:
        print("\nHealth check failed!")
        exit(1)

    print("\nTesting authentication requirements...")
    test_auth_required()

    print("\nTesting chat API endpoint...")
    test_chat_api()

    print("\nTest completed. The chatbot functionality requires authentication.")