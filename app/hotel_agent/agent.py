from google.adk.agents import Agent
from app.hotel_agent.sub_agents.booking_agent import booking_agent
from app.hotel_agent.sub_agents.concierge_agent import concierge_agent
from app.hotel_agent.tools.escalation_tools import escalate_to_human
from app.config import GEMINI_MODEL

root_agent = Agent(
    name="hotel_root_agent",
    model=GEMINI_MODEL,
    description="The main router for the hotel assistant. It delegates tasks to specialized agents.",
    instruction="""
    You are the primary assistant for a hotel. Your job is to understand the user's request and delegate it to the correct specialist agent.

    - For any questions about **booking a room, checking availability, or sales**, delegate to the `booking_agent`.
    - For questions about **hotel information, amenities, or nearby attractions**, delegate to the `concierge_agent`.
    - If the user expresses a **complaint, is angry, or asks for a manager**, use the `escalate_to_human` tool immediately.

    If you are unsure, ask a clarifying question.
    """,
    sub_agents=[booking_agent, concierge_agent],
    tools=[escalate_to_human]
)