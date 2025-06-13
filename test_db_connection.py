# test_db_connection.py

import os
import psycopg2
from dotenv import load_dotenv

print("--- Starting Minimal Database Connection Test ---")

# Load the exact same .env file your app uses
print("Loading .env file...")
load_dotenv()

# Get the database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("!!! ERROR: DATABASE_URL not found in .env file. Please check your .env file.")
else:
    print(f"Found DATABASE_URL. Attempting to connect...")
    # Print the URL without the password for security
    safe_url = DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL
    print(f"Connecting to: ...@{safe_url}")
    
    conn = None
    try:
        # Try to connect directly using psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        
        # If the line above doesn't crash, the connection is successful
        print("\n✅✅✅ SUCCESS! Database connection established successfully. ✅✅✅")
        
        # Let's run a simple query to be sure
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"PostgreSQL Version: {db_version[0]}")
        cursor.close()

    except psycopg2.OperationalError as e:
        print("\n❌❌❌ FAILURE! The minimal connection test failed. ❌❌❌")
        print("This confirms the issue is with the environment, not the application code.")
        print("\n--- Error Details ---")
        print(e)
        print("---------------------")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

    finally:
        if conn is not None:
            conn.close()
            print("\nConnection closed.")

print("\n--- Test Complete ---")