# Data Model: AI Chatbot for Todo Management

**Feature**: AI Chatbot for Todo Management
**Date**: 2026-01-15
**Status**: Complete

## Entity Definitions

### Conversation
Represents a user's chat session with the AI assistant.

**Fields**:
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key to users table)
- `title`: String (Generated from first message or "New Conversation")
- `created_at`: DateTime (Timestamp)
- `updated_at`: DateTime (Timestamp)
- `is_active`: Boolean (Default: true)

**Validation Rules**:
- `user_id` must reference an existing user
- `created_at` is set on creation
- `updated_at` is updated on any changes

**State Transitions**:
- Active → Archived (when conversation is closed)

### Message
Represents an individual chat message within a conversation.

**Fields**:
- `id`: UUID (Primary Key)
- `conversation_id`: UUID (Foreign Key to conversations table)
- `role`: Enum ('user' | 'assistant')
- `content`: Text (The message content)
- `timestamp`: DateTime (Timestamp)
- `metadata`: JSON (Additional data like tool calls, etc.)

**Validation Rules**:
- `conversation_id` must reference an existing conversation
- `role` must be either 'user' or 'assistant'
- `content` length must be between 1 and 10,000 characters
- `timestamp` is set on creation

### Todo (Extended)
Existing todo entity with additional fields to support chatbot functionality.

**Fields**:
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key to users table)
- `title`: String
- `description`: Text (Optional)
- `due_date`: Date (Optional)
- `status`: Enum ('incomplete' | 'complete')
- `created_at`: DateTime (Timestamp)
- `updated_at`: DateTime (Timestamp)
- `source`: Enum ('manual' | 'chatbot') (Default: 'manual')

**Validation Rules**:
- `user_id` must reference an existing user
- `title` length must be between 1 and 255 characters
- `status` must be either 'incomplete' or 'complete'

## Relationships

### User ↔ Conversation
- One-to-Many relationship
- User can have multiple conversations
- Foreign key: `user_id` in conversations table

### Conversation ↔ Message
- One-to-Many relationship
- Conversation can have multiple messages
- Foreign key: `conversation_id` in messages table

### User ↔ Todo
- One-to-Many relationship
- User can have multiple todos
- Foreign key: `user_id` in todos table

## Indexes

### Conversations Table
- Index on `user_id` for efficient user-based queries
- Index on `user_id` and `is_active` for active conversation queries

### Messages Table
- Index on `conversation_id` for conversation-based queries
- Index on `conversation_id` and `timestamp` for chronological ordering

### Todos Table
- Index on `user_id` for user-based queries
- Index on `user_id` and `status` for status-filtered queries
- Index on `user_id` and `due_date` for date-filtered queries

## Constraints

### Referential Integrity
- All foreign key relationships enforce cascading behavior as appropriate
- User deletion removes associated conversations and messages
- Conversation deletion removes associated messages

### Data Validation
- All timestamps are stored in UTC
- Text fields are properly sanitized to prevent injection
- Role field is restricted to allowed values only

## Access Control

### Row-Level Security
- Users can only access their own conversations and messages
- Users can only modify their own todos through the chatbot
- Assistant messages are read-only to users

### Query Patterns

#### Common Queries
1. Get all active conversations for a user
2. Get all messages in a conversation ordered by timestamp
3. Get todos for a user filtered by status/due date
4. Create a new conversation with initial message

#### Performance Considerations
- Pagination implemented for message lists
- Conversation previews avoid loading full message history
- Bulk operations supported for todo management