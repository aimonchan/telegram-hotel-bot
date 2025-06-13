from google.adk.agents import Agent
from app.hotel_agent.tools.info_tools import get_attractions
from app.config import GEMINI_MODEL

concierge_agent = Agent(
    name="concierge_agent",
    model=GEMINI_MODEL,
    description="Answers general questions about the hotel, room types, and nearby attractions.",
    instruction="""
    You are a friendly and helpful hotel concierge.
    Use `get_attractions` to tell users about interesting places nearby.
    Answer questions about hotel policies and amenities based on your general knowledge.
    """,
    tools=[get_attractions],
)