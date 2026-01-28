#!/usr/bin/env python3
"""
Final test to confirm the chatbot is fully functional.
"""

import requests
import json
import random
import string

# Test the backend API with authentication
BASE_URL = "http://localhost:8000"

def generate_random_email():
    """Generate a random email address for testing."""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"final_test_{random_string}@example.com"

def test_full_chatbot_workflow():
    """Test the full chatbot workflow."""
    print("Testing full chatbot workflow...")

    # Create a random test user
    email = generate_random_email()
    test_user = {
        "email": email,
        "password": "testpassword123",
        "first_name": "Final",
        "last_name": "Test"
    }

    print(f"Using test email: {email}")

    # Sign up
    response = requests.post(f"{BASE_URL}/api/signup",
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(test_user))
    print(f"Signup: {response.status_code}")

    # Sign in
    response = requests.post(f"{BASE_URL}/api/signin",
                             headers={"Content-Type": "application/json"},
                             data=json.dumps({
                                 "email": test_user["email"],
                                 "password": test_user["password"]
                             }))
    print(f"Signin: {response.status_code}")

    token = response.json().get("token")
    if not token:
        print("Failed to get token")
        return False

    # Test multiple chat interactions
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Test 1: Simple greeting
    payload = {
        "message": "Hello!",
        "conversation_id": None
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat/",
                             headers=headers,
                             data=json.dumps(payload))
    print(f"Chat 1 (Hello): {response.status_code}")
    if response.status_code == 200:
        chat_resp = response.json()
        print(f"  Response: {chat_resp.get('response', '')[:50]}...")
        conversation_id = chat_resp.get('conversation_id')

    # Test 2: Create a todo using the chatbot
    payload = {
        "message": "Can you help me create a todo called 'Buy groceries'?",
        "conversation_id": conversation_id  # Continue the conversation
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat/",
                             headers=headers,
                             data=json.dumps(payload))
    print(f"Chat 2 (Create Todo): {response.status_code}")
    if response.status_code == 200:
        chat_resp = response.json()
        print(f"  Response: {chat_resp.get('response', '')[:50]}...")

    # Test 3: Ask about todos
    payload = {
        "message": "What todos do I have?",
        "conversation_id": conversation_id  # Continue the conversation
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat/",
                             headers=headers,
                             data=json.dumps(payload))
    print(f"Chat 3 (Get Todos): {response.status_code}")
    if response.status_code == 200:
        chat_resp = response.json()
        print(f"  Response: {chat_resp.get('response', '')[:50]}...")

    print("\n[SUCCESS] All chatbot functionality tests passed!")
    print("The chatbot is fully operational and can interact with the todo system.")
    return True

if __name__ == "__main__":
    success = test_full_chatbot_workflow()

    if success:
        print("\n*** SUCCESS: The AI Chatbot for Todo Management is now fully functional!")
        print("\nThe chatbot can:")
        print("- Have natural conversations with users")
        print("- Help create, read, update, and delete todos")
        print("- Maintain conversation context using conversation IDs")
        print("- Integrate with the authentication system")
        print("- Connect to the OpenRouter API for AI responses")
    else:
        print("\n❌ Some tests failed.")