#!/usr/bin/env python3
"""
Test the position-based deletion functionality.
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
    return f"pos_test_{random_string}@example.com"

def test_position_based_deletion():
    """Test position-based deletion functionality."""
    print("Testing position-based deletion functionality...")

    # Create a random test user
    email = generate_random_email()
    test_user = {
        "email": email,
        "password": "testpassword123",
        "first_name": "Position",
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

    # Add multiple todos to test position-based deletion
    print("\n--- Adding multiple todos ---")

    # Add first todo
    payload1 = {
        "message": 'add todo "First todo for position test"',
        "conversation_id": None
    }
    response1 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload1))
    print(f"Added first todo: {response1.status_code}")

    # Add second todo
    payload2 = {
        "message": 'add todo "Second todo for position test"',
        "conversation_id": response1.json().get('conversation_id')
    }
    response2 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload2))
    print(f"Added second todo: {response2.status_code}")

    # Add third todo
    payload3 = {
        "message": 'add todo "Third todo for position test"',
        "conversation_id": response2.json().get('conversation_id')
    }
    response3 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload3))
    print(f"Added third todo: {response3.status_code}")

    # Check all todos
    print("\n--- Checking all todos ---")
    payload_check = {
        "message": "what todos do I have?",
        "conversation_id": response3.json().get('conversation_id')
    }
    response_check = requests.post(f"{BASE_URL}/api/v1/chat/",
                                  headers=headers,
                                  data=json.dumps(payload_check))
    print(f"Check todos response: {response_check.status_code}")
    if response_check.status_code == 200:
        check_data = response_check.json()
        print(f"All todos: {check_data.get('response', '')[:300]}...")
        conversation_id = check_data.get('conversation_id')

    # Test position-based deletion (delete the first todo at position 1)
    print("\n--- Testing position-based deletion: delete position 1 ---")
    payload_delete_pos1 = {
        "message": 'delete the todo at position 1',
        "conversation_id": conversation_id
    }
    response_delete_pos1 = requests.post(f"{BASE_URL}/api/v1/chat/",
                                         headers=headers,
                                         data=json.dumps(payload_delete_pos1))
    print(f"Delete position 1 response: {response_delete_pos1.status_code}")
    if response_delete_pos1.status_code == 200:
        delete_data1 = response_delete_pos1.json()
        print(f"Delete pos 1 result: {delete_data1.get('response', '')[:100]}...")

    # Check remaining todos
    print("\n--- Checking remaining todos after deleting position 1 ---")
    response_check2 = requests.post(f"{BASE_URL}/api/v1/chat/",
                                   headers=headers,
                                   data=json.dumps(payload_check))
    if response_check2.status_code == 200:
        check_data2 = response_check2.json()
        print(f"Remaining todos: {check_data2.get('response', '')[:300]}...")

    # Test the original problematic command: "delete todo 'hi' id: 1"
    print("\n--- Testing original problematic command: 'delete todo \"Second todo for position test\" id: 1' ---")
    # First add a todo named "hi" to match the original issue
    payload_add_hi = {
        "message": 'add todo "hi"',
        "conversation_id": response_check2.json().get('conversation_id')
    }
    response_add_hi = requests.post(f"{BASE_URL}/api/v1/chat/",
                                   headers=headers,
                                   data=json.dumps(payload_add_hi))
    print(f"Added 'hi' todo: {response_add_hi.status_code}")

    # Check todos again
    response_check3 = requests.post(f"{BASE_URL}/api/v1/chat/",
                                   headers=headers,
                                   data=json.dumps(payload_check))
    if response_check3.status_code == 200:
        check_data3 = response_check3.json()
        print(f"Todos before deletion: {check_data3.get('response', '')[:300]}...")

    # Now try the position-based deletion using the new functionality
    print("\n--- Trying 'delete todo at position 1' (equivalent to 'id: 1') ---")
    payload_pos_del = {
        "message": 'delete todo at position 1',
        "conversation_id": check_data3.get('conversation_id')
    }
    response_pos_del = requests.post(f"{BASE_URL}/api/v1/chat/",
                                    headers=headers,
                                    data=json.dumps(payload_pos_del))
    print(f"Position deletion response: {response_pos_del.status_code}")
    if response_pos_del.status_code == 200:
        pos_del_data = response_pos_del.json()
        print(f"Position deletion result: {pos_del_data.get('response', '')[:200]}...")

    print("\n[POSITION-BASED DELETION TEST COMPLETED]")
    return True

if __name__ == "__main__":
    success = test_position_based_deletion()

    if success:
        print("\n*** POSITION-BASED DELETION TESTING COMPLETE ***")
        print("Testing position-based deletion functionality.")
    else:
        print("\n❌ Position-based deletion test failed.")