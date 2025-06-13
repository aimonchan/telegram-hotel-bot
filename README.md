# hotel_adk_bot
hotel-telegram-bot/
├── .env                  # Environment variables (DB URL, API keys)
├── .gitignore
├── requirements.txt      # Python dependencies
├── render.yaml           # Render.com deployment configuration
│
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI web server and Telegram webhook endpoint
│   ├── config.py           # Central configuration settings
│   ├── database.py         # SQLAlchemy models and database session setup
│   ├── telegram_utils.py   # Helpers for sending messages to Telegram
│   │
│   └── hotel_agent/
│       ├── __init__.py
│       ├── agent.py          # Defines the root agent and its sub-agents
│       │
│       ├── sub_agents/
│       │   ├── __init__.py
│       │   ├── booking_agent.py
│       │   └── concierge_agent.py
│       │
│       └── tools/
│           ├── __init__.py
│           ├── booking_tools.py   # Check availability, book rooms (DB write)
│           ├── info_tools.py      # Get room details, search attractions
│           └── escalation_tools.py# Handle human handoff