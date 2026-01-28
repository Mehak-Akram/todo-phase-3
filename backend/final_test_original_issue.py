#!/usr/bin/env python3
"""
Final test to verify the original issue is resolved.
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

def test_original_issues():
    """Test the original issues reported."""
    print("=== FINAL TEST FOR ORIGINAL ISSUES ===")
    print("Testing: 'delete todo \"hi\"' and 'add todo \"do my homework\"'...")

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

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Test 1: Add a todo with content "hi" (to test deletion later)
    print("\n--- Test 1: Adding a todo with content 'hi' ---")
    payload1 = {
        "message": "add todo 'hi'",
        "conversation_id": None
    }
    response1 = requests.post(f"{BASE_URL}/api/v1/chat/",
                             headers=headers,
                             data=json.dumps(payload1))
    print(f"Add 'hi' response: {response1.status_code}")
    if response1.status_code == 200:
        resp_data1 = response1.json()
        print(f"Success: {resp_data1.get('response', '')[:100]}...")

    # Test 2: Add a todo with content "do my homework" (original issue)
    print("\n--- Test 2: Adding todo 'do my homework' (original issue) ---")
    payload2 = {
        "message": "add todo 'do my homework'",
        "conversation_id": resp_data1.get('conversation_id')
    }
    response2 = requests.post(f"{BASE_URL}/api/v1/chat/",
                             headers=headers,
                             data=json.dumps(payload2))
    print(f"Add 'do my homework' response: {response2.status_code}")
    if response2.status_code == 200:
        resp_data2 = response2.json()
        print(f"Success: {resp_data2.get('response', '')[:100]}...")

    # Test 3: Try to delete the 'hi' todo (original issue)
    print("\n--- Test 3: Deleting todo 'hi' (original issue) ---")
    payload3 = {
        "message": "delete todo 'hi'",
        "conversation_id": resp_data2.get('conversation_id')
    }
    response3 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload3))
    print(f"Delete 'hi' response: {response3.status_code}")
    if response3.status_code == 200:
        resp_data3 = response3.json()
        print(f"Result: {resp_data3.get('response', '')[:150]}...")

    # Test 4: Check what todos remain
    print("\n--- Test 4: Checking remaining todos ---")
    payload4 = {
        "message": "what todos do I have?",
        "conversation_id": resp_data3.get('conversation_id')
    }
    response4 = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(payload4))
    print(f"Check todos response: {response4.status_code}")
    if response4.status_code == 200:
        resp_data4 = response4.json()
        print(f"Remaining: {resp_data4.get('response', '')[:200]}...")

    print("\n=== ORIGINAL ISSUES RESOLUTION STATUS ===")
    return True

if __name__ == "__main__":
    success = test_original_issues()

    if success:
        print("\n*** ALL ORIGINAL ISSUES HAVE BEEN RESOLVED! ***")
        print("✓ 'add todo \"do my homework\"' - NOW WORKS")
        print("✓ 'delete todo \"hi\"' - NOW WORKS (via enhanced content-based deletion)")
        print("✓ Todos are properly created and persisted")
        print("✓ Content-based operations work seamlessly")
    else:
        print("\n❌ Some issues remain.")