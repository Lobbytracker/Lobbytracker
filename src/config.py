import os

# Ai folder's variables
AITTA_URL = "https://aitta-api.csc.fi"
DEFAULT_MODEL = "openai/gpt-oss-120b"
REQUEST_TIMEOUT_SECONDS = 300
MAX_API_CALL_ATTEMPTS = 2
MIN_PROMPT_LENGTH = 20
BATCH_MAX_RERUNS = 2

DEFAULT_PROMPT = (
        "Determine whether the following concept appears in the document. "
        "The stance label (Yes/No) in front of the concept tells you whether "
        "the concept promotes or opposes the climate law. "
        "If it does, give the passage from the document that expresses it, "
        "quoted exactly as written, without markdown or ellipses. "
        "The passage may endorse or reject the argument. "
        "Set agreement to true if the author endorses the argument, "
        "and false if the author rejects it. "
        "If the concept is not found, set present to false, passage to null, "
        "and agreement to null. "
        'Do not answer "yes" unless you can provide a supporting passage.'
)
# DB folder's variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/lobbytracker",
)
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/lobbytracker_test",
)

# Tui:
BACK_TO_MENU_COMMANDS = {"b"}
