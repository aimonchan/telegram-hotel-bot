from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, ForeignKey, DATE, TIMESTAMP, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from .config import DATABASE_URL

# Create the single, correctly configured engine here
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_size=5, # Good practice for server apps
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Models
class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    room_type = Column(String(50), nullable=False)
    price_per_night = Column(DECIMAL(10, 2), nullable=False)
    availability = Column(String(20), default='available')

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    check_in_date = Column(DATE, nullable=False)
    check_out_date = Column(DATE, nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    booking_status = Column(String(20), default='confirmed')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

# Function to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()