# ==============================================================================
# 1. SET ENVIRONMENT FOR SSL - THIS MUST BE THE VERY FIRST THING
# ==============================================================================
import os
import certifi
# This line forces Python and all its libraries (like psycopg2) to use
# the SSL certificates provided by the certifi package. This is the most
# reliable way to fix SSL handshake errors on all operating systems.
os.environ['SSL_CERT_FILE'] = certifi.where()
# ==============================================================================

# 2. NOW, IMPORT EVERYTHING ELSE
import asyncio
import json
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai.types import Content, Part

from .config import ADK_APP_NAME, DATABASE_URL, TELEGRAM_TOKEN
from app.hotel_agent.agent import root_agent # Using relative import
from .telegram_utils import send_telegram_message, set_telegram_webhook


# --- 3. Initialize ADK Components ---
# This will now work correctly because the SSL environment is fixed.
print("Initializing ADK DatabaseSessionService...")
try:
    session_service = DatabaseSessionService(
        db_url=DATABASE_URL,
        connect_args={"sslmode": "require"} # Explicitly require SSL
    )
    print("ADK DatabaseSessionService initialized successfully.")
except Exception as e:
    print("!!!!!!!!!! FAILED TO INITIALIZE ADK SESSION SERVICE !!!!!!!!!!")
    print(f"Error: {e}")
    # In a real app, you might want the app to fail to start here.
    # For now, we'll let it continue but it will fail on the first request.
    session_service = None

if session_service:
    runner = Runner(
        agent=root_agent,
        app_name=ADK_APP_NAME,
        session_service=session_service,
    )
else:
    runner = None # Ensure runner is None if service failed

# --- FastAPI Lifespan Manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup logic, like setting the Telegram webhook."""
    print("Application startup...")
    if not runner:
        print("!!! WARNING: ADK Runner not initialized due to database connection issue.")
    await asyncio.sleep(2)
    await set_telegram_webhook()
    yield
    print("Application shutdown...")

# --- Create FastAPI App Instance ---
app = FastAPI(lifespan=lifespan)

# --- Webhook Endpoint for Telegram ---
@app.post("/webhook/{token}")
async def process_telegram_update(token: str, request: Request):
    if not runner:
        print("ERROR: Cannot process request because ADK Runner is not available.")
        # Optionally, send a message back to the user
        # await send_telegram_message(chat_id, "Sorry, the bot is currently experiencing technical difficulties.")
        raise HTTPException(status_code=503, detail="Service is temporarily unavailable due to a configuration error.")
        
    # The rest of your webhook logic...
    # ... (This can remain as it was) ...
    print("\n--- NEW WEBHOOK REQUEST RECEIVED ---")
    try:
        # ... your full webhook logic here ...
        # (This part of your code seems fine)
        if token != TELEGRAM_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid token")

        data = await request.json()
        message = data.get("message")
        if not message or not message.get("text"):
            return {"status": "ok"}
        
        chat_id = message["chat"]["id"]
        user_text = message["text"]

        content = Content(role="user", parts=[Part(text=user_text)])
        
        final_response_text = "I'm sorry, an error occurred during processing."
        async for event in runner.run_async(user_id=str(chat_id), session_id=str(chat_id), new_message=content):
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
    
        await send_telegram_message(chat_id, final_response_text)
        return {"status": "ok"}
    except Exception as e:
        traceback.print_exc()
        return {"status": "error"}


# --- Health Check Endpoint ---
@app.get("/")
def health_check():
    """A simple endpoint to confirm the server is running."""
    return {"status": "ok", "message": "ADK Hotel Bot is running"}