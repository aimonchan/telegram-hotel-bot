# In app/hotel_agent/tools/__init__.py
from .booking_tools import check_room_availability, book_room
from .info_tools import get_attractions
from .escalation_tools import escalate_to_human

# This makes it easy for other files to import all tools from one place
__all__ = [
    "check_room_availability",
    "book_room",
    "get_attractions",
    "escalate_to_human",
]