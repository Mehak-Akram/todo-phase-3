#!/usr/bin/env python3
"""
Test to check if todos are actually persisted in the database after chatbot creates them.
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
    return f"persist_test_{random_string}@example.com"

def test_todo_persistence():
    """Test if todos are actually persisted after chatbot creation."""
    print("Testing todo persistence after chatbot creation...")

    # Create a random test user
    email = generate_random_email()
    test_user = {
        "email": email,
        "password": "testpassword123",
        "first_name": "Persist",
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

    auth_response = response.json()
    token = auth_response.get("token")
    user_id = auth_response.get("user", {}).get("id")

    if not token:
        print("Failed to get token")
        return False

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Step 1: Check initial todos (should be empty)
    print("\n--- Step 1: Checking initial todos ---")
    todos_response = requests.get(f"{BASE_URL}/api/todos/", headers=headers)
    print(f"Initial todos API: {todos_response.status_code}")
    if todos_response.status_code == 200:
        initial_todos = todos_response.json()
        print(f"Initial todos count: {len(initial_todos)}")

    # Step 2: Create a todo via chatbot
    print("\n--- Step 2: Creating todo via chatbot ---")
    payload = {
        "message": "Create a todo called 'Test homework assignment'",
        "conversation_id": None
    }
    chat_response = requests.post(f"{BASE_URL}/api/v1/chat/",
                                 headers=headers,
                                 data=json.dumps(payload))
    print(f"Chat API (create todo): {chat_response.status_code}")
    if chat_response.status_code == 200:
        chat_resp = chat_response.json()
        print(f"  Chat response: {chat_resp.get('response', '')[:100]}...")
        conversation_id = chat_resp.get('conversation_id')

    # Step 3: Check todos via chatbot again
    print("\n--- Step 3: Asking chatbot for todos ---")
    payload2 = {
        "message": "What todos do I have?",
        "conversation_id": conversation_id
    }
    chat_response2 = requests.post(f"{BASE_URL}/api/v1/chat/",
                                  headers=headers,
                                  data=json.dumps(payload2))
    print(f"Chat API (get todos): {chat_response2.status_code}")
    if chat_response2.status_code == 200:
        chat_resp2 = chat_response2.json()
        print(f"  Chat response: {chat_resp2.get('response', '')[:100]}...")

    # Step 4: Check todos via direct API call
    print("\n--- Step 4: Checking todos via direct API ---")
    todos_response2 = requests.get(f"{BASE_URL}/api/todos/", headers=headers)
    print(f"Direct todos API: {todos_response2.status_code}")
    if todos_response2.status_code == 200:
        final_todos = todos_response2.json()
        print(f"Final todos count: {len(final_todos)}")
        for i, todo in enumerate(final_todos):
            print(f"  Todo {i+1}: {todo.get('content', 'No content')} (completed: {todo.get('completed', 'N/A')})")

    print("\n--- Analysis ---")
    if len(initial_todos) == 0 and len(final_todos) > 0:
        print("[SUCCESS] Todo was successfully created and persisted!")
        print(f"   Todo created: {final_todos[0].get('content', 'Unknown')}")
    elif len(initial_todos) == 0 and len(final_todos) == 0:
        print("[ISSUE] Chatbot said it created a todo, but it's not in the database!")
        print("   This confirms the reported issue.")
    else:
        print(f"   Info: Starting with {len(initial_todos)} todos, ending with {len(final_todos)} todos")

    return True

if __name__ == "__main__":
    success = test_todo_persistence()

    if success:
        print("\n[ANALYSIS COMPLETE]")
    else:
        print("\n❌ Persistence test failed.")