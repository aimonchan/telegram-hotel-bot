import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# ADK
ADK_APP_NAME = "HotelTelegramBot"
GEMINI_MODEL = "gemini-2.0-flash"

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL")

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

# Simple checks to ensure critical variables are set
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set.")