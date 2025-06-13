from google.adk.agents import Agent
from app.hotel_agent.tools.booking_tools import check_room_availability, book_room
from app.config import GEMINI_MODEL

booking_agent = Agent(
    name="booking_agent",
    model=GEMINI_MODEL,
    description="Handles all tasks related to checking room availability and booking rooms.",
    instruction="""
    You are a specialized booking assistant.
    1. Use `check_room_availability` to see if rooms are free.
    2. Use `book_room` to finalize a booking.
    3. Confirm the booking details and total price to the user upon success.
    4. You must get the check-in and check-out dates to perform any action.
    """,
    tools=[check_room_availability, book_room],
)