#!/usr/bin/env python3
"""
Test the specific issues mentioned by the user.
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
    return f"specific_test_{random_string}@example.com"

def test_specific_issues():
    """Test the specific issues mentioned by the user."""
    print("Testing specific issues mentioned by user...")

    # Create a random test user
    email = generate_random_email()
    test_user = {
        "email": email,
        "password": "testpassword123",
        "first_name": "Specific",
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

    # Test 1: Try the exact command mentioned by user
    print("\n--- Test 1: Testing 'add todo \"to my homework\" title: do math home work' ---")
    payload1 = {
        "message": 'add todo "to my homework" title: do math home work',
        "conversation_id": None
    }
    response1 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload1))
    print(f"Response: {response1.status_code}")
    if response1.status_code == 200:
        resp_data1 = response1.json()
        print(f"Chat response: {resp_data1.get('response', '')[:150]}...")
        conversation_id = resp_data1.get('conversation_id')

    # Check what todos exist now
    print("\n--- Check: What todos exist after creation? ---")
    payload_check = {
        "message": "what todos do I have?",
        "conversation_id": conversation_id
    }
    response_check = requests.post(f"{BASE_URL}/api/v1/chat/",
                                  headers=headers,
                                  data=json.dumps(payload_check))
    if response_check.status_code == 200:
        check_data = response_check.json()
        print(f"Todos: {check_data.get('response', '')[:200]}...")

    # Test 2: Try the exact deletion command mentioned by user
    print("\n--- Test 2: Testing 'delete todo \"hi\" id: 1' ---")
    # First, let's add a todo named "hi" to test with
    payload_add_hi = {
        "message": 'add todo "hi"',
        "conversation_id": conversation_id
    }
    response_add_hi = requests.post(f"{BASE_URL}/api/v1/chat/",
                                   headers=headers,
                                   data=json.dumps(payload_add_hi))
    print(f"Add 'hi' response: {response_add_hi.status_code}")

    # Check current todos to see their IDs
    response_check2 = requests.post(f"{BASE_URL}/api/v1/chat/",
                                   headers=headers,
                                   data=json.dumps(payload_check))
    if response_check2.status_code == 200:
        check_data2 = response_check2.json()
        print(f"Todos after adding 'hi': {check_data2.get('response', '')[:300]}...")

    # Now try the deletion command
    payload2 = {
        "message": 'delete todo "hi" id: 1',
        "conversation_id": check_data2.get('conversation_id')
    }
    response2 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload2))
    print(f"Delete response: {response2.status_code}")
    if response2.status_code == 200:
        resp_data2 = response2.json()
        print(f"Delete response: {resp_data2.get('response', '')[:200]}...")

    # Final check
    print("\n--- Final Check: Remaining todos ---")
    response_final = requests.post(f"{BASE_URL}/api/v1/chat/",
                                  headers=headers,
                                  data=json.dumps(payload_check))
    if response_final.status_code == 200:
        final_data = response_final.json()
        print(f"Final todos: {final_data.get('response', '')[:200]}...")

    print("\n[SPECIFIC ISSUES TEST COMPLETED]")
    return True

if __name__ == "__main__":
    success = test_specific_issues()

    if success:
        print("\n*** SPECIFIC ISSUES TESTED ***")
        print("Analyze the output to see current behavior vs expected behavior.")
    else:
        print("\n❌ Specific issues test failed.")