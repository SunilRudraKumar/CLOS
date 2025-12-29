import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application Configuration
    Reads from environment variables (or .env file).
    """
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "CLOS - Cognitive Logistics Operating System"
    
    # Celery / Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AI / LLM Keys
    GOOGLE_API_KEY: str = "" # Required for Gemini 1.5 Flash
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/clos_db"
    
    # Supabase (Storage & DB)
    SUPABASE_URL: str = "" 
    SUPABASE_KEY: str = ""
    
    # Security
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
