import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    API_URL = os.getenv("API_URL")
    API_KEY = f"Bearer {os.getenv('API_KEY')}"
    ADMIN_ID = int(os.getenv("ADMIN_ID"))


