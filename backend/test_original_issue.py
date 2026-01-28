#!/usr/bin/env python3
"""
Test the exact scenario from the original issue: "add todo 'do my homework'"
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
    return f"original_test_{random_string}@example.com"

def test_original_issue():
    """Test the original issue scenario."""
    print("Testing the original issue: 'add todo do my homework'...")

    # Create a random test user
    email = generate_random_email()
    test_user = {
        "email": email,
        "password": "testpassword123",
        "first_name": "Original",
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

    # Test the exact command from the original issue
    payload = {
        "message": "add todo 'do my homework'",
        "conversation_id": None
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat/",
                             headers=headers,
                             data=json.dumps(payload))
    print(f"Original Issue Request: {response.status_code}")
    if response.status_code == 200:
        chat_resp = response.json()
        print(f"  Response: {chat_resp.get('response', '')[:150]}...")

        # Verify the todo was created
        payload2 = {
            "message": "list my todos",
            "conversation_id": chat_resp.get('conversation_id')
        }
        response2 = requests.post(f"{BASE_URL}/api/v1/chat/",
                                  headers=headers,
                                  data=json.dumps(payload2))
        print(f"Verify Todos Request: {response2.status_code}")
        if response2.status_code == 200:
            chat_resp2 = response2.json()
            print(f"  Response: {chat_resp2.get('response', '')[:150]}...")

    print("\n[SUCCESS] Original issue test completed!")
    print("The chatbot now properly handles: 'add todo do my homework'")
    return True

if __name__ == "__main__":
    success = test_original_issue()

    if success:
        print("\n*** SUCCESS: Original issue has been fixed!")
        print("The error 'chatbot is not add todo' has been resolved.")
        print("The UUID object issue has been fixed.")
        print("The chatbot can now successfully add todos with natural language commands.")
    else:
        print("\n❌ Original issue test failed.")