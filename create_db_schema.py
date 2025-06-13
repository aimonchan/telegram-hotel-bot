# create_db_schema.py
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import time

# Load environment variables from .env file
print("Loading environment variables...")
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please check your .env file.")

# The SQL code to execute
SQL_SCHEMA_SCRIPT = """
    CREATE TABLE IF NOT EXISTS rooms (
        id SERIAL PRIMARY KEY,
        room_type VARCHAR(50) NOT NULL,
        price_per_night DECIMAL(10, 2) NOT NULL,
        availability VARCHAR(20) DEFAULT 'available'
    );

    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE NOT NULL,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS bookings (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        room_id INTEGER NOT NULL REFERENCES rooms(id),
        check_in_date DATE NOT NULL,
        check_out_date DATE NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL,
        booking_status VARCHAR(20) DEFAULT 'confirmed',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- Check if rooms table is empty before inserting
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM rooms) THEN
            INSERT INTO rooms (room_type, price_per_night, availability) VALUES
            ('Standard', 150.00, 'available'),
            ('Standard', 150.00, 'available'),
            ('Deluxe', 250.00, 'available'),
            ('Suite', 400.00, 'occupied');
        END IF;
    END $$;
"""

def setup_database():
    """Connects to the database and executes the schema setup script."""
    print(f"Connecting to the database...")
    
    # Retry connection for a few seconds as DB might be starting up
    for attempt in range(5):
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect() as connection:
                print("Connection successful. Creating schema...")
                connection.execute(text(SQL_SCHEMA_SCRIPT))
                connection.commit()
                print("Database schema and initial data created successfully!")
                return
        except Exception as e:
            print(f"Connection failed (Attempt {attempt + 1}/5): {e}")
            if attempt < 4:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("Could not connect to the database after several attempts.")
                raise

if __name__ == "__main__":
    setup_database()