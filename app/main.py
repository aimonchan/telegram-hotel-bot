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
from .hotel_agent.agent import root_agent # Make sure this path matches your folder structure
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
# In app/main.py

@app.post("/webhook/{token}")
async def process_telegram_update(token: str, request: Request):
    """This endpoint receives all incoming messages from Telegram."""
    print("\n--- NEW WEBHOOK REQUEST RECEIVED ---")
    if not runner:
        print("ERROR: Cannot process request because ADK Runner is not available.")
        raise HTTPException(status_code=503, detail="Service is temporarily unavailable due to a configuration error.")

    try:
        # 1. Authenticate and parse the request
        if token != TELEGRAM_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid token")

        data = await request.json()
        message = data.get("message")
        if not message or not message.get("text"):
            return {"status": "ok"}
        
        chat_id = message["chat"]["id"]
        user_text = message["text"]
        print(f"--- INFO: Processing message from Chat ID: {chat_id}, Text: '{user_text}'")

        # --------------------- THE FINAL CORRECTED LOGIC ---------------------
        # 2. Explicitly get the session and check if it exists.
        user_id = str(chat_id)
        session_id = str(chat_id)
        
        print(f"--- INFO: Checking for existing ADK session for user_id: {user_id}")
        # 'await' is critical here
        session = await session_service.get_session(app_name=ADK_APP_NAME, user_id=user_id, session_id=session_id)

        # Now, explicitly check if the session is None (or falsy)
        if not session:
            print(f"--- INFO: Session not found. Creating a new one...")
            # 'await' is critical here too
            session = await session_service.create_session(app_name=ADK_APP_NAME, user_id=user_id, session_id=session_id)
            print(f"--- INFO: New session created successfully.")
        else:
            print(f"--- INFO: Existing session found and loaded.")
        # -----------------------------------------------------------------------

        # 3. Process the message with the ADK Agent Runner
        print(f"--- INFO: Calling ADK Runner for user_id: {user_id}...")
        content = Content(role="user", parts=[Part(text=user_text)])
        
        final_response_text = "I'm sorry, I encountered a problem. Please try again."
        
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            print(f"--- DEBUG: Agent Event [Author: {event.author}]")
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
    
        # 4. Send the final response back to the user
        print(f"--- INFO: Agent generated final response: '{final_response_text}'")
        await send_telegram_message(chat_id, final_response_text)
        print("--- INFO: Response sent to Telegram. ---")

        return {"status": "ok"}
    except Exception as e:
        print(f"\n!!!!!!!!!! A CRITICAL UNEXPECTED ERROR OCCURRED IN WEBHOOK !!!!!!!!!!")
        print(f"Critical Error: {e}")
        traceback.print_exc()
        return {"status": "error", "detail": "An internal server error occurred."}


# --- Health Check Endpoint ---
@app.get("/")
def health_check():
    """A simple endpoint to confirm the server is running."""
    return {"status": "ok", "message": "ADK Hotel Bot is running"}