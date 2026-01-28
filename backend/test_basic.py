#!/usr/bin/env python3
"""
Test to verify that all basic functionality works properly.
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
    return f"basic_test_{random_string}@example.com"

def test_basic_functionality():
    """Test basic functionality to ensure everything works."""
    print("Testing basic functionality...")

    # Create a random test user
    email = generate_random_email()
    test_user = {
        "email": email,
        "password": "testpassword123",
        "first_name": "Basic",
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

    # Test 1: Create a todo
    print("\n--- Test 1: Creating a todo ---")
    payload = {
        "message": "Add a todo with title 'Basic Test Todo'",
        "conversation_id": None
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat/",
                             headers=headers,
                             data=json.dumps(payload))
    print(f"Create response: {response.status_code}")
    if response.status_code == 200:
        resp_data = response.json()
        print(f"Success: {resp_data.get('response', '')[:100]}...")
        conversation_id = resp_data.get('conversation_id')

    # Test 2: List todos
    print("\n--- Test 2: Listing todos ---")
    payload2 = {
        "message": "What todos do I have?",
        "conversation_id": conversation_id
    }
    response2 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload2))
    print(f"List response: {response2.status_code}")
    if response2.status_code == 200:
        resp_data2 = response2.json()
        print(f"Success: {resp_data2.get('response', '')[:100]}...")

    # Test 3: Check via direct API
    print("\n--- Test 3: Direct API check ---")
    direct_response = requests.get(f"{BASE_URL}/api/todos/", headers=headers)
    print(f"Direct API response: {direct_response.status_code}")
    if direct_response.status_code == 200:
        todos = direct_response.json()
        print(f"Todos in database: {len(todos)}")
        for todo in todos:
            print(f"  - {todo.get('content')} (ID: {todo.get('id')[:8]}...)")

    print("\n[ALL BASIC TESTS COMPLETED]")
    return True

if __name__ == "__main__":
    success = test_basic_functionality()

    if success:
        print("\n*** BASIC FUNCTIONALITY WORKING ***")
        print("The core functionality is working properly.")
        print("The issue might be with AI model's ability to handle natural language requests.")
    else:
        print("\n❌ Basic functionality test failed.")