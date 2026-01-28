# Deploy to Hugging Face Spaces

This guide explains how to deploy the Todo App with AI Chatbot to Hugging Face Spaces using Docker.

## Prerequisites

1. A Hugging Face account
2. Repository pushed to Hugging Face Hub
3. API keys for external services (OpenRouter, etc.)

## Deployment Steps

### 1. Prepare Your Repository

Make sure your repository contains:
- `Dockerfile` (or `Dockerfile.hf` renamed to `Dockerfile`)
- `space.yaml`
- Source code in the `src/` directory
- `requirements.txt`

### 2. Configure Environment Variables

In your Hugging Face Space settings, go to "Secrets" and add:

```
OPENROUTER_API_KEY=your_openrouter_api_key
SECRET_KEY=your_secure_secret_key
BETTER_AUTH_SECRET=your_auth_secret
```

### 3. Create the Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose:
   - **Space SDK**: Docker
   - **GPU**: No GPU (or CPU only)
   - **Hardware**: Choose appropriate CPU/Memory based on your needs
4. Connect to your repository

### 4. Environment Configuration

The Docker image will automatically use SQLite for database persistence and look for the required environment variables in the Space secrets.

### 5. Build and Run

The Space will automatically build using the Dockerfile and start the FastAPI application on port 8000.

## Important Notes

- The application uses SQLite for Hugging Face Spaces (persistent storage)
- For production deployments, consider using PostgreSQL
- API keys should be stored in Space Secrets, not committed to the repository
- The database file will persist in the Space's storage volume

## Troubleshooting

If the Space fails to build:
1. Check the build logs for errors
2. Ensure all dependencies in `requirements.txt` are compatible
3. Verify that required environment variables are set in Space Secrets

If the application fails to start:
1. Check the runtime logs
2. Verify database connection
3. Ensure all required environment variables are set