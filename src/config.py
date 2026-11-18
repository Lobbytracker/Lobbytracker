import os

# Ai folder's variables
AITTA_URL = "https://aitta-api.csc.fi"
DEFAULT_MODEL = "openai/gpt-oss-120b"
REQUEST_TIMEOUT_SECONDS = 300
MAX_API_CALL_ATTEMPTS = 2

# DB folder's variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/lobbytracker",
)

# Tui:
BACK_TO_MENU_COMMANDS = {"b"}
