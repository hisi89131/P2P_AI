from telethon import TelegramClient
from config import API_ID, API_HASH

user_client = TelegramClient(
    "user_session",
    API_ID,
    API_HASH
)

bot = TelegramClient(
    "bot_session",
    API_ID,
    API_HASH
)
