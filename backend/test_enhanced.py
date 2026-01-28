#!/usr/bin/env python3
"""
Test the enhanced functionality that can handle content-based operations.
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
    return f"enh_test_{random_string}@example.com"

def test_enhanced_functionality():
    """Test enhanced functionality with content-based operations."""
    print("Testing enhanced functionality with content-based operations...")

    # Create a random test user
    email = generate_random_email()
    test_user = {
        "email": email,
        "password": "testpassword123",
        "first_name": "Enhanced",
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
        "message": "Add a todo with title 'Test Delete Operation'",
        "conversation_id": None
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat/",
                             headers=headers,
                             data=json.dumps(payload))
    print(f"Create response: {response.status_code}")
    if response.status_code == 200:
        resp_data = response.json()
        print(f"Success: {repr(resp_data.get('response', '')[:100])}...")
        conversation_id = resp_data.get('conversation_id')

    # Test 2: Try to delete by content (the original issue)
    print("\n--- Test 2: Deleting by content (original issue) ---")
    payload2 = {
        "message": "delete todo 'Test Delete Operation'",
        "conversation_id": conversation_id
    }
    response2 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload2))
    print(f"Delete by content response: {response2.status_code}")
    if response2.status_code == 200:
        resp_data2 = response2.json()
        print(f"Response: {repr(resp_data2.get('response', ''))[:200]}...")

    # Test 3: Check if todo still exists
    print("\n--- Test 3: Verifying deletion ---")
    payload3 = {
        "message": "What todos do I have?",
        "conversation_id": conversation_id
    }
    response3 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload3))
    print(f"Check remaining todos: {response3.status_code}")
    if response3.status_code == 200:
        resp_data3 = response3.json()
        print(f"Remaining todos: {repr(resp_data3.get('response', ''))[:200]}...")

    # Test 4: Create another todo and try update by content
    print("\n--- Test 4: Creating another todo for update test ---")
    payload4 = {
        "message": "Add a todo with title 'Test Update Operation'",
        "conversation_id": conversation_id
    }
    response4 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload4))
    print(f"Create for update test: {response4.status_code}")
    if response4.status_code == 200:
        resp_data4 = response4.json()
        print(f"Success: {repr(resp_data4.get('response', '')[:100])}...")

    # Test 5: Try to update by content
    print("\n--- Test 5: Updating by content ---")
    payload5 = {
        "message": "Change the todo 'Test Update Operation' to 'Updated Todo Successfully'",
        "conversation_id": conversation_id
    }
    response5 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload5))
    print(f"Update by content response: {response5.status_code}")
    if response5.status_code == 200:
        resp_data5 = response5.json()
        print(f"Update response: {repr(resp_data5.get('response', ''))[:200]}...")

    # Test 6: Verify the update happened
    print("\n--- Test 6: Verifying update ---")
    response6 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload3))  # Reuse check payload
    print(f"Check updated todos: {response6.status_code}")
    if response6.status_code == 200:
        resp_data6 = response6.json()
        print(f"Updated todos: {repr(resp_data6.get('response', ''))[:200]}...")

    print("\n[ENHANCED FUNCTIONALITY TEST COMPLETED]")
    return True

if __name__ == "__main__":
    success = test_enhanced_functionality()

    if success:
        print("\n*** ENHANCED FUNCTIONALITY TESTING COMPLETE ***")
        print("Testing content-based operations (delete by content, update by content).")
    else:
        print("\n❌ Enhanced functionality test failed.")