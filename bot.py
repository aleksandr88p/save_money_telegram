import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from bot.config import Config
from core.handlers import basic, callback
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command

import contextvars

current_bot = contextvars.ContextVar('current_bot')

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

async def start_bot(bot: Bot):
    """
    Уведомление для администратора, что бот запущен.
    """
    await bot.send_message(Config.ADMIN_ID, "Бот запущен!")

async def stop_bot(bot: Bot):
    """
    Уведомление для администратора, что бот остановлен.
    """
    await bot.send_message(Config.ADMIN_ID, "Бот остановлен!")

async def start():
    """
    Запуск бота и регистрация команд
    """
    current_bot.set(bot)

    # Подключение middleware, если нужно
    dp.message.middleware(ChatActionMiddleware())

    # Регистрация команд
    dp.message.register(basic.send_welcome, Command(commands=['start', 'run']))
    dp.message.register(basic.get_help, Command(commands=['help']))

    # Регистрация callback для переключения языка
    dp.callback_query.register(callback.switch_to_russian, lambda c: c.data == 'switch_to_russian')
    dp.callback_query.register(callback.switch_to_english, lambda c: c.data == 'switch_to_english')

    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())
