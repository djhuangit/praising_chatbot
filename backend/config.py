from pydantic_settings import BaseSettings
from typing import List
import os
from functools import lru_cache

class Settings(BaseSettings):
    # Base configuration
    PROJECT_NAME: str = "Praising Chat API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./kuakuaqun.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "https://djpraisingchat.netlify.app",  # Production
        "http://localhost:5173",               # Local development
        "http://127.0.0.1:5173",              # Alternative local development
    ]
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

    @property
    def is_production(self) -> bool:
        return "pythonanywhere.com" in os.environ.get("PYTHONANYWHERE_DOMAIN", "")

    @property
    def is_development(self) -> bool:
        return not self.is_production

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Create a global settings instance
settings = get_settings() 