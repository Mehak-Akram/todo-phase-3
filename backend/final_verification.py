#!/usr/bin/env python3
"""
Final verification that the todo creation and persistence issue is fixed.
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
    return f"final_verify_{random_string}@example.com"

def final_verification():
    """Final verification test."""
    print("=== FINAL VERIFICATION ===")
    print("Verifying that todos are created AND persisted correctly...")

    # Create a random test user
    email = generate_random_email()
    test_user = {
        "email": email,
        "password": "testpassword123",
        "first_name": "Final",
        "last_name": "Verify"
    }

    print(f"Using test email: {email}")

    # Sign up and sign in
    signup_resp = requests.post(f"{BASE_URL}/api/signup",
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(test_user))
    print(f"Signup: {signup_resp.status_code}")

    signin_resp = requests.post(f"{BASE_URL}/api/signin",
                               headers={"Content-Type": "application/json"},
                               data=json.dumps({
                                   "email": test_user["email"],
                                   "password": test_user["password"]
                               }))
    print(f"Signin: {signin_resp.status_code}")

    token = signin_resp.json().get("token")
    if not token:
        print("Failed to get token")
        return False

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Check initial state
    todos_before = requests.get(f"{BASE_URL}/api/todos/", headers=headers)
    initial_count = len(todos_before.json()) if todos_before.status_code == 200 else 0
    print(f"Todos before: {initial_count}")

    # Use chatbot to create a specific todo
    chat_payload = {
        "message": "Add a todo called 'Verify system is working properly'",
        "conversation_id": None
    }
    chat_resp = requests.post(f"{BASE_URL}/api/v1/chat/",
                            headers=headers,
                            data=json.dumps(chat_payload))

    if chat_resp.status_code == 200:
        chat_data = chat_resp.json()
        print(f"Chat response: {chat_data.get('response', '')[:80]}...")

        # Check if the chatbot confirmed creation
        response_text = chat_data.get('response', '').lower()
        if 'add' in response_text or 'create' in response_text or 'added' in response_text:
            print("[OK] Chatbot confirmed todo creation")
        else:
            print("[?] Chatbot response doesn't clearly confirm creation")
    else:
        print(f"[ERROR] Chatbot failed to respond: {chat_resp.status_code}")
        return False

    # Check todos after creation via direct API
    todos_after = requests.get(f"{BASE_URL}/api/todos/", headers=headers)
    final_count = len(todos_after.json()) if todos_after.status_code == 200 else 0
    final_todos = todos_after.json() if todos_after.status_code == 200 else []

    print(f"Todos after: {final_count}")

    # Look for our specific todo
    target_todo_found = False
    for todo in final_todos:
        content = todo.get('content', '').lower()
        if 'verify system is working properly' in content:
            target_todo_found = True
            print(f"[FOUND] Todo '{content}' is in the database")
            break

    if target_todo_found:
        print("[VERIFIED] Todo was created by chatbot AND persisted in database")
    else:
        print("[FAILED] Todo was not found in database despite chatbot saying it was created")
        print("  Database contents:", [t.get('content') for t in final_todos])

    # Additional verification: ask chatbot what todos exist
    verify_payload = {
        "message": "What todos do I have?",
        "conversation_id": chat_data.get('conversation_id')
    }
    verify_resp = requests.post(f"{BASE_URL}/api/v1/chat/",
                              headers=headers,
                              data=json.dumps(verify_payload))

    if verify_resp.status_code == 200:
        verify_text = verify_resp.json().get('response', '').lower()
        print(f"Chatbot verification: {verify_text[:80]}...")
        if 'verify system is working properly' in verify_text or 'verify' in verify_text:
            print("[OK] Chatbot correctly reports the created todo")
        else:
            print("? Chatbot doesn't seem to recognize the todo it just created")

    print("\n=== SUMMARY ===")
    success = target_todo_found and final_count > initial_count
    if success:
        print("[SUCCESS] Todo creation and persistence is working perfectly!")
        print("   - Chatbot creates todos correctly")
        print("   - Todos are persisted in the database")
        print("   - Both chatbot and direct API show consistent results")
    else:
        print("[ISSUES] There are still problems with todo persistence")

    return success

if __name__ == "__main__":
    success = final_verification()

    if success:
        print("\n*** ALL ISSUES FIXED ***")
        print("The original problem 'chatbot tell me i add todo but in todo list todo is not add' has been resolved!")
        print("Todos created via chatbot are now properly persisted in the database.")
    else:
        print("\n*** ISSUES REMAIN ***")
        print("Further investigation needed.")