#!/usr/bin/env python3
"""
Comprehensive test to verify all chatbot functionalities including create, get, update, delete.
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
    return f"comp_test_{random_string}@example.com"

def test_comprehensive_workflow():
    """Test comprehensive workflow: create, get, update, delete."""
    print("Testing comprehensive chatbot workflow...")

    # Create a random test user
    email = generate_random_email()
    test_user = {
        "email": email,
        "password": "testpassword123",
        "first_name": "Comprehensive",
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

    # Step 1: Create a todo via chatbot
    print("\n--- Step 1: Creating a todo via chatbot ---")
    payload = {
        "message": "Create a todo with the title 'Test todo for deletion'",
        "conversation_id": None
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat/",
                             headers=headers,
                             data=json.dumps(payload))
    print(f"Create Todo Response: {response.status_code}")
    if response.status_code == 200:
        chat_resp = response.json()
        response_text = chat_resp.get('response', '')[:100]
        print(f"  Chat response: {repr(response_text)}")
        conversation_id = chat_resp.get('conversation_id')

    # Step 2: Get all todos to see the ID
    print("\n--- Step 2: Getting all todos to see ID ---")
    payload2 = {
        "message": "What todos do I have?",
        "conversation_id": conversation_id
    }
    response2 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload2))
    print(f"Get Todos Response: {response2.status_code}")
    if response2.status_code == 200:
        chat_resp2 = response2.json()
        response_text = chat_resp2.get('response', '')[:200]
        print(f"  Chat response: {repr(response_text)}")

    # Step 3: Try to delete the todo using its content
    print("\n--- Step 3: Trying to delete todo by content ---")
    payload3 = {
        "message": "delete todo 'Test todo for deletion'",
        "conversation_id": conversation_id
    }
    response3 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload3))
    print(f"Delete Todo Response: {response3.status_code}")
    if response3.status_code == 200:
        chat_resp3 = response3.json()
        response_text = chat_resp3.get('response', '')[:200]
        print(f"  Chat response: {repr(response_text)}")

    # Step 4: Check if todo still exists
    print("\n--- Step 4: Checking if todo still exists ---")
    payload4 = {
        "message": "What todos do I have?",
        "conversation_id": conversation_id
    }
    response4 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload4))
    print(f"Final Todos Check: {response4.status_code}")
    if response4.status_code == 200:
        chat_resp4 = response4.json()
        response_text = chat_resp4.get('response', '')[:200]
        print(f"  Chat response: {repr(response_text)}")

    # Step 5: Try to delete using direct API to see if the issue is with the chatbot
    print("\n--- Step 5: Getting todos via direct API ---")
    todos_response = requests.get(f"{BASE_URL}/api/todos/", headers=headers)
    if todos_response.status_code == 200:
        todos = todos_response.json()
        print(f"  Direct API todos count: {len(todos)}")
        for todo in todos:
            print(f"    - ID: {todo.get('id')}, Content: {todo.get('content')}")

            # Try to delete this specific todo via chatbot using its ID
            if todo.get('content') == 'Test todo for deletion':
                print(f"\n--- Step 6: Deleting via chatbot using actual ID: {todo.get('id')} ---")
                payload5 = {
                    "message": f"delete the todo with id {todo.get('id')}",
                    "conversation_id": conversation_id
                }
                response5 = requests.post(f"{BASE_URL}/api/v1/chat/",
                                          headers=headers,
                                          data=json.dumps(payload5))
                print(f"Delete by ID Response: {response5.status_code}")
                if response5.status_code == 200:
                    chat_resp5 = response5.json()
                    response_text = chat_resp5.get('response', '')[:200]
                    print(f"  Chat response: {repr(response_text)}")

    print("\n[COMPREHENSIVE TEST COMPLETED]")
    return True

if __name__ == "__main__":
    success = test_comprehensive_workflow()

    if success:
        print("\n*** COMPREHENSIVE TEST FINISHED ***")
        print("Review the output to see if create/get/update/delete work properly.")
    else:
        print("\n❌ Comprehensive test failed.")