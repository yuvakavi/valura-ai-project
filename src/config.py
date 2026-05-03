import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-test-key")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
APP_ENV = os.getenv("APP_ENV", "development")
