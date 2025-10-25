"""
Configuration loader for Telegram AI Assistant.
Loads tokens and API keys from environment variables or .env file.
If keys are missing, mock mode is enabled.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    GMAIL_API_KEY: str
    GOOGLE_CALENDAR_API_KEY: str
    BASEROW_API_KEY: str
    mock: bool

    @staticmethod
    def load_from_env() -> "Config":
        tg = os.getenv("TELEGRAM_BOT_TOKEN", "")
        oa = os.getenv("OPENAI_API_KEY", "")
        gm = os.getenv("GMAIL_API_KEY", "")
        gc = os.getenv("GOOGLE_CALENDAR_API_KEY", "")
        br = os.getenv("BASEROW_API_KEY", "")
        mock = not (tg and oa and gm and gc and br)

        return Config(
            TELEGRAM_BOT_TOKEN=tg,
            OPENAI_API_KEY=oa,
            GMAIL_API_KEY=gm,
            GOOGLE_CALENDAR_API_KEY=gc,
            BASEROW_API_KEY=br,
            mock=mock
        )
