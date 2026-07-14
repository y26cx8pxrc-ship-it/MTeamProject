import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

SLOT_LIMIT = 5  # максимум мест на один слот

if not BOT_TOKEN:
    raise ValueError("Переменная BOT_TOKEN не найдена в .env")

env_array_str = os.getenv('ADMINS', "")
if env_array_str:
    ADMINS = list(map(int, env_array_str.split(',')))
else:
    ADMINS = []