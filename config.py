"""
config.py
---------
Loads environment variables (API key, model name) and exposes them
as simple constants for the rest of the app to use.
"""

import os
from dotenv import load_dotenv

# Load variables from a .env file in the project root, if present.
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


class ConfigError(Exception):
    """Raised when required configuration (e.g. API key) is missing."""


def validate_config() -> None:
    """
    Confirms the API key has actually been set.
    Called once at startup so we fail fast with a clear message
    instead of a confusing error from deep inside the API client.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
        raise ConfigError(
            "GEMINI_API_KEY is missing or not set.\n"
            "1. Copy .env.example to .env\n"
            "2. Get a free key from https://aistudio.google.com/apikey\n"
            "3. Paste it into .env as GEMINI_API_KEY=your_key_here"
        )