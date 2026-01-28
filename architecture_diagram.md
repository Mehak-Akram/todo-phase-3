# Todo Application Architecture Diagram

## Overview
This document describes the architecture of the Todo application with integrated chatbot functionality.

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   Database      │
│   (Next.js)     │    │   (FastAPI)      │    │   (SQLite)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                        │
         │ 1. Create Todo        │                        │
         │ ─────────────────────▶│                        │
         │                       │ 2. Call todo_service   │
         │                       │ ─────────────────────▶ │
         │                       │                        │
         │                       │ 3. Create Todo Record│
         │                       │ ◀───────────────────── │
         │                       │                        │
         │ 4. Receive Response   │                        │
         │ ◀─────────────────────│                        │
         │                       │                        │
         │                       │                        │
         │ 5. Chatbot Request    │                        │
         │ ─────────────────────▶│                        │
         │                       │ 6. AI Processing &    │
         │                       │    Tool Calling       │
         │                       │ ─────────────────────▶ │
         │                       │                        │
         │                       │ 7. Create Todo via    │
         │                       │    same service       │
         │                       │ ─────────────────────▶ │
         │                       │                        │
         │ 8. Refresh UI         │                        │
         │ ◀─────────────────────│                        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Data Flow for Todo Creation

### 1. UI-Based Creation
- User enters todo in UI form
- `handleAddTodo()` calls `todoAPI.createTodo()`
- Backend receives request at `/api/todos`
- `todo_service.create_todo()` creates record in database
- Response returns to UI with new todo data
- UI updates state immediately: `setTodos([response.data, ...todos])`

### 2. Chatbot-Based Creation
- User types message in chat interface requesting todo creation
- `ChatWindow.handleSendMessage()` sends to `/api/v1/chat`
- Backend processes with AI agent using function calling
- `CreateTodoTool.execute()` calls same `todo_service.create_todo()`
- AI responds with success message
- Chatbot triggers `onTodoChange()` callback
- UI refreshes todos with fresh API call to ensure sync

## Key Components

### Frontend Components
- `pages/todos/index.tsx`: Main todo page with UI and chatbot integration
- `components/Chatbot/ChatWindow.tsx`: Chat interface with improved detection logic
- `components/Chatbot/ChatbotFloatingIcon.tsx`: Access point for chatbot
- `services/api.ts`: API client for standard todo operations
- `services/api/chatApi.ts`: API client for chat operations

### Backend Components
- `api/todos.py`: Standard REST API endpoints
- `api/chat_api.py`: Chat endpoints with conversation management
- `services/chat_service.py`: Chat message processing
- `services/agent_service.py`: AI integration with function calling
- `services/todo_service.py`: Shared service layer for all todo operations
- `tools/create_todo_tool.py`: AI tool for creating todos
- `models/todo.py`: Todo data model with SQLAlchemy/SQLModel

## Problem & Solution

### Problem
Chatbot-created todos were not appearing in the main UI because:
1. Timing issues between backend processing and UI refresh
2. Inconsistent detection of todo creation actions in AI responses
3. Variable delays in triggering UI refresh after chatbot actions

### Solution Implemented
1. **Consistent Timing**: Increased delay to 1000ms to ensure database transactions complete
2. **Improved Detection**: Enhanced `checkIfTodoAction()` with regex patterns and broader term matching
3. **Guaranteed Refresh**: Added fallback refresh in finally block to ensure UI sync regardless of detection success
4. **Enhanced Callback**: Improved error handling and logging in `onTodoChange` callback

## Security & Authentication
- JWT-based authentication for all endpoints
- User-specific data isolation
- Secure API communication with token validation

## Technologies Used
- **Frontend**: Next.js, React, Tailwind CSS
- **Backend**: FastAPI, Python
- **Database**: SQLite with SQLModel
- **AI Integration**: OpenRouter API with function calling
- **Authentication**: JWT tokens