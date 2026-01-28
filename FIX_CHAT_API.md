# Fix for Chat API Database Schema Issue

## Problem
The chat API was failing with "Failed to send message. Please try again." due to a database schema mismatch. The database contained a `thread_id` column in the `conversation` table with a NOT NULL constraint, but the application model wasn't providing values for this field.

## Root Cause
The alembic migrations were not properly applied to the database. The migration file `d9b25f58a7c3_add_due_date_column_to_todo_table.py` is designed to remove the `thread_id` column from the conversation table, but the database still had the column.

## Temporary Fix Applied
Modified the application code to:
1. Updated the Conversation model to include the `thread_id` field
2. Ensured the field is populated with a unique UUID during conversation creation
3. Updated the Message model to properly handle the `metadata_json` field

## Permanent Solution
To properly fix this issue, run the following commands to apply the migrations:

```bash
cd backend
alembic merge -m "merge migration heads"  # This resolves the multiple head issue
alembic upgrade head  # This applies all pending migrations
```

Or if there are multiple heads, you may need to:
1. Identify the correct migration path
2. Mark one as the head: `alembic stamp <correct_revision_id>`
3. Then run: `alembic upgrade head`

## Files Modified
- backend/src/models/conversation.py
- backend/src/services/chat_service.py

## Testing
The fix has been tested and the chat API now works without the database constraint error.