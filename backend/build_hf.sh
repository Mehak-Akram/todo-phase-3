#!/bin/bash
# Build script for Hugging Face Space deployment

echo "Building Docker image for Hugging Face Space..."

# Build the Docker image
docker build -t todo-app-hf .

echo "Docker image built successfully!"
echo ""
echo "To test locally, run:"
echo "  docker run -p 8000:8000 -e OPENROUTER_API_KEY='your-key-here' todo-app-hf"
echo ""
echo "For Hugging Face Space deployment:"
echo "1. Push your repository to Hugging Face Hub"
echo "2. Add OPENROUTER_API_KEY as a secret in your Space settings"
echo "3. Ensure space.yaml is configured properly"