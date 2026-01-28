from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, todos
from .api.chat_api import router as chat_router
from .database.database import create_db_and_tables
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Todo API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001",
                   "http://localhost:3002", "http://localhost:3003"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api")
app.include_router(todos.router, prefix="/api")
app.include_router(chat_router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    try:
        create_db_and_tables()
    except Exception as e:
        print(f"Database initialization error: {e}")
        # Continue startup even if DB init fails to avoid blocking the app

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}