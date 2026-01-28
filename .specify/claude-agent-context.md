# Todo Full-Stack Application Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-15

## Active Technologies

Python 3.11, TypeScript/Next.js, OpenAI Agents SDK, FastAPI, React, PostgreSQL (Neon Serverless), pytest, Jest

## Project Structure

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py      # Conversation and message models
│   │   └── todo.py              # Todo models (extended from existing)
│   ├── services/
│   │   ├── agent_service.py     # AI agent orchestration
│   │   ├── chat_service.py      # Chat API business logic
│   │   └── todo_service.py      # Todo operations via tools
│   ├── tools/
│   │   ├── create_todo_tool.py
│   │   ├── get_todos_tool.py
│   │   ├── update_todo_tool.py
│   │   ├── delete_todo_tool.py
│   │   └── set_todo_status_tool.py
│   └── api/
│       └── chat_api.py          # Chat API endpoints
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/
│   │   └── Chatbot/
│   │       ├── ChatWindow.tsx
│   │       ├── Message.tsx
│   │       └── InputArea.tsx
│   ├── pages/
│   │   └── chat/
│   └── services/
│       └── api/
│           └── chatApi.ts
└── tests/
    ├── unit/
    └── integration/
```

## Commands

### Backend
- `uvicorn src.main:app --reload --port 8000` - Start backend server
- `pytest tests/` - Run all backend tests
- `python -m src.database.migrate` - Apply database migrations

### Frontend
- `npm run dev` - Start frontend development server
- `npm test` - Run all frontend tests

### Database
- `psql` connection with DATABASE_URL environment variable

## Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Write docstrings for public functions/classes
- Use async/await for asynchronous operations

### TypeScript/React
- Use functional components with hooks
- Follow React best practices for state management
- Use TypeScript interfaces for props and data structures
- Implement proper error boundaries

### Database
- Use SQLModel for ORM operations
- Follow consistent naming conventions (snake_case for tables/columns)
- Implement proper indexing strategies
- Use transactions for multi-step operations

## Recent Changes

1. **AI Chatbot for Todo Management** - Added AI-powered chatbot interface allowing natural language todo management with conversation history, new data models for conversations/messages, and integration with OpenAI Agents SDK.

2. **Phase II Authentication** - Implemented user authentication system with JWT tokens and user data isolation.

3. **Todo Management System** - Core functionality for creating, viewing, updating, and deleting todos with due dates and status tracking.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->