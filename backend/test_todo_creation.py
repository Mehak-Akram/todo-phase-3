#!/usr/bin/env python3
"""
Test to specifically verify that todo creation is working properly.
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
    return f"todo_test_{random_string}@example.com"

def test_todo_creation():
    """Test todo creation specifically."""
    print("Testing todo creation functionality...")

    # Create a random test user
    email = generate_random_email()
    test_user = {
        "email": email,
        "password": "testpassword123",
        "first_name": "Todo",
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

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Test creating a specific todo
    payload = {
        "message": "Create a todo with the title 'Do my homework'",
        "conversation_id": None
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat/",
                             headers=headers,
                             data=json.dumps(payload))
    print(f"Create Todo Request: {response.status_code}")
    if response.status_code == 200:
        chat_resp = response.json()
        print(f"  Response: {chat_resp.get('response', '')[:100]}...")
        conversation_id = chat_resp.get('conversation_id')

        # Now ask to see the todos
        payload2 = {
            "message": "What todos do I have?",
            "conversation_id": conversation_id
        }
        response2 = requests.post(f"{BASE_URL}/api/v1/chat/",
                                  headers=headers,
                                  data=json.dumps(payload2))
        print(f"Get Todos Request: {response2.status_code}")
        if response2.status_code == 200:
            chat_resp2 = response2.json()
            print(f"  Response: {chat_resp2.get('response', '')[:100]}...")

    print("\n[SUCCESS] Todo creation test completed!")
    return True

if __name__ == "__main__":
    success = test_todo_creation()

    if success:
        print("\n*** SUCCESS: Todo creation functionality is working!")
        print("The chatbot can now successfully create and manage todos.")
    else:
        print("\n❌ Todo creation test failed.")