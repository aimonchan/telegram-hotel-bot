import httpx
from .config import TELEGRAM_TOKEN, WEBHOOK_BASE_URL

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

async def send_telegram_message(chat_id: int, text: str):
    """Sends a text message to a Telegram user."""
    async with httpx.AsyncClient() as client:
        payload = {"chat_id": chat_id, "text": text}
        response = await client.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)
        if response.status_code != 200:
            print(f"Error sending message to Telegram: {response.text}")
        return response

async def set_telegram_webhook():
    """Sets the Telegram bot webhook to the deployed URL."""
    webhook_url = f"{WEBHOOK_BASE_URL}/webhook/{TELEGRAM_TOKEN}"
    async with httpx.AsyncClient() as client:
        payload = {"url": webhook_url}
        response = await client.post(f"{TELEGRAM_API_URL}/setWebhook", json=payload)
        if response.status_code == 200:
            print(f"Webhook set successfully to: {webhook_url}")
        else:
            print(f"Failed to set webhook: {response.text}")