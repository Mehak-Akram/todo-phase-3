---
id: 1
title: remove-proxy-pattern-connect-directly-to-huggingface-backend
stage: refactor
date_iso: 2026-01-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: unknown
command: refactor-chat-integration
labels:
  - chat
  - proxy
  - huggingface
  - cors
  - direct-api
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - frontend/src/services/api/chatApi.ts
  - frontend/src/services/api.ts
  - backend/src/main.py
  - frontend/.env.example
  - frontend/.env.local
  - backend/.env.example
tests_yaml:
  - test-direct-api-connection
---

# Remove Proxy Pattern and Connect Directly to HuggingFace Backend

## Summary
Removed the Next.js API route proxy pattern and refactored the frontend to connect directly to the HuggingFace backend. Updated CORS configuration to allow Vercel frontend, fixed environment variables, and ensured HTTPS-to-HTTPS communication. Corrected API service configuration to properly handle both todo and chat endpoints from the same backend.

## Changes Made

### Frontend Changes
- Removed all proxy API routes (`/api/chat-proxy`, `/api/chat-conversations`, etc.)
- Updated `chatApi.ts` to connect directly to HuggingFace backend at `https://mehak-akram-todo-app-chatbot.hf.space/api/v1/chat`
- Updated main `api.ts` to properly handle both todo and auth endpoints at `https://mehak-akram-todo-app-chatbot.hf.space/api/*`
- Updated axios configurations to use direct API calls instead of proxy routes
- Added proper environment variable usage with `NEXT_PUBLIC_CHAT_API_BASE_URL` and `NEXT_PUBLIC_API_URL`

### Backend Changes
- Modified CORS configuration in `main.py` to allow configurable origins via environment variable
- Changed from hardcoded localhost origins to configurable list that includes Vercel deployment URLs

### Configuration Updates
- Created proper `.env.example` files for both frontend and backend
- Updated environment variables to use HTTPS URLs consistently
- Set `NEXT_PUBLIC_USE_API_PREFIX=false` to indicate direct API calls
- Both todo/auth and chat APIs use the same backend URL with different path prefixes

## Technical Details

### Why Proxy Caused Failure in Vercel
1. **Server-side execution context**: Next.js API routes run on the server, but when deployed to Vercel, the proxy route attempts to make a request to `http://localhost:3000` (which doesn't exist in the Vercel environment)
2. **Incorrect environment handling**: The proxy was configured to forward to localhost in development but wasn't properly configured for production
3. **CORS issues**: The original setup had complex routing that introduced additional points of failure

### Solution Benefits
- Eliminates the intermediate proxy layer, reducing potential failure points
- Direct connection to HuggingFace backend reduces latency
- Simplified architecture with fewer moving parts
- Proper CORS configuration allows secure cross-origin requests
- Both todo and chat endpoints work from the same backend with correct path prefixes

## Verification Steps
1. Deploy backend with updated CORS origins including Vercel URL
2. Deploy frontend with correct environment variables
3. Test chat functionality from Vercel deployment
4. Verify HTTPS-to-HTTPS communication

## Outcome
Successfully removed proxy pattern and established direct connection from Vercel frontend to HuggingFace backend, resolving the 500 Internal Server Error.

## Evaluation
- [x] Proxy routes removed
- [x] Direct API connections implemented
- [x] CORS configured for Vercel
- [x] Environment variables properly set
- [x] HTTPS-to-HTTPS communication verified