import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

SLOT_LIMIT = 5  # максимум мест на один слот

if not BOT_TOKEN:
    raise ValueError("Переменная BOT_TOKEN не найдена в .env")

ADMINS = [
    123456789,  # <-- сюда свой Telegram ID
]