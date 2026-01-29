from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "")
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"

    # OpenRouter Configuration
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "google/gemini-pro")

    # CORS Configuration
    cors_origins: str = os.getenv("CORS_ORIGINS", "")

settings = Settings()