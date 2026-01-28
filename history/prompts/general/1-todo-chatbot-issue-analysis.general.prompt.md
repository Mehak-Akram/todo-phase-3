---
id: 1
title: Todo Chatbot Issue Analysis
stage: explainer
date: 2026-01-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 1-ai-chatbot-todos
user: user
command: analyze todo chatbot issue
labels: ["todo", "chatbot", "ui-sync", "troubleshooting"]
---

# Todo Chatbot Issue Analysis

## User Query
User reported that when they asked the chatbot to "play cirket", it should create a todo but it's not showing up in their todo app.

## Investigation
After analyzing the codebase, I found that the AI chatbot is designed to recognize specific trigger phrases when creating todos. The phrase "play cirket" alone doesn't contain the keywords the AI looks for to identify a todo creation request.

## Root Cause
The AI is programmed to recognize phrases like:
- "add todo"
- "create todo"
- "add task"
- "create task"
- "make todo"
- "new todo"
- "remind me to"

## Solution
To create a todo via the chatbot, users need to use one of these formats:
- "Add a todo to play cirket"
- "Create a todo to play cirket"
- "Add task: play cirket"
- "Create a task to play cirket"

## Outcome
The backend server is running correctly and the functionality is in place - it just needs the right phrasing for the AI to recognize the intent to create a todo. The UI sync functionality is working properly as well.

## Files Referenced
- backend\src\services\agent_service.py
- backend\src\tools\create_todo_tool.py
- frontend\src\components\Chatbot\ChatWindow.tsx
- backend\test_todo_creation.py
- backend\test_chat_api.py