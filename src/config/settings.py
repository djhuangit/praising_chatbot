"""Application settings and configuration"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Demo Mode Configuration
# Default to true if not explicitly set to false
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY and not DEMO_MODE:
    raise ValueError("OpenAI API key not found in environment variables. Set OPENAI_API_KEY or set DEMO_MODE=true for testing")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "7860"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

# Application Configuration
APP_TITLE = "Praising Chatbot"
APP_VERSION = "0.3.0"
APP_DESCRIPTION = "A supportive chatbot with FastAPI backend and Gradio frontend"

# Chatbot Configuration
SYSTEM_PROMPT = """You are a supportive and encouraging friend. Your role is to provide positive,
uplifting responses that make the user feel good about themselves and their achievements.
Always maintain a positive, humorous and fluffy tone and keep the responses within 50 words. No emoji."""

# Cost Configuration
COST_PER_MILLION_TOKENS = 0.15  # For gpt-4o-mini
