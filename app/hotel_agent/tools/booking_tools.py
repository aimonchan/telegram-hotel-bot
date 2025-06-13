from sqlalchemy.orm import Session
from google.adk.tools import ToolContext
from app.database import get_db, Room, Booking, User
from datetime import datetime, timedelta

def check_room_availability(room_type: str, check_in_date: str, check_out_date: str) -> dict:
    """Checks for available rooms of a specific type for given dates."""
    db: Session = next(get_db())
    available_rooms = db.query(Room).filter(
        Room.room_type == room_type,
        Room.availability == 'available'
    ).all()
    # This is a simplified check. A real system would check for booking overlaps.
    if available_rooms:
        return {"status": "success", "available_count": len(available_rooms), "price": available_rooms[0].price_per_night}
    return {"status": "error", "message": f"No available '{room_type}' rooms for those dates."}

def book_room(room_type: str, check_in_date: str, check_out_date: str, tool_context: ToolContext) -> dict:
    """Books an available room for a user and updates its status to 'occupied'."""
    db: Session = next(get_db())
    try:
        # Find an available room
        room_to_book = db.query(Room).filter(
            Room.room_type == room_type,
            Room.availability == 'available'
        ).first()

        if not room_to_book:
            return {"status": "error", "message": "Sorry, no rooms of that type are available."}

        # Get user from telegram_id (stored in ADK user_id)
        telegram_id = int(tool_context.user_id)
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            return {"status": "error", "message": "User not found."}

        # Mark room as occupied
        room_to_book.availability = 'occupied'
        
        # Create booking record
        check_in = datetime.strptime(check_in_date, "%Y-%m-%d").date()
        check_out = datetime.strptime(check_out_date, "%Y-%m-%d").date()
        duration = (check_out - check_in).days
        total_price = duration * room_to_book.price_per_night

        new_booking = Booking(
            user_id=user.id,
            room_id=room_to_book.id,
            check_in_date=check_in,
            check_out_date=check_out,
            total_price=total_price
        )
        db.add(new_booking)
        db.commit()

        return {
            "status": "success",
            "message": f"Successfully booked a {room_type} room.",
            "booking_id": new_booking.id,
            "total_price": float(total_price)
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"An error occurred during booking: {e}"}
    finally:
        db.close()