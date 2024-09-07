import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from bot.config import Config
from core.handlers import basic, callback, audio_handler, confirm_handler, submit_handler, query_handler
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram import F
from core.states import AudioState, TextState, QueryState

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
    dp.message.register(audio_handler.audio_command, Command(commands=["audio"]))
    dp.message.register(audio_handler.handle_voice, F.content_type == 'voice', AudioState.waiting_for_audio_expenses)
    dp.message.register(submit_handler.handle_submit_command, Command(commands=['submit']))
    dp.message.register(submit_handler.handle_text_submission, TextState.waiting_for_text)
    dp.message.register(query_handler.handle_query_command, Command(commands=['query']))
    dp.message.register(query_handler.handle_query_submission, QueryState.waiting_for_query)

    # Регистрация callback для переключения языка
    dp.callback_query.register(callback.switch_to_russian, lambda c: c.data == 'switch_to_russian')
    dp.callback_query.register(callback.switch_to_english, lambda c: c.data == 'switch_to_english')

    dp.callback_query.register(callback.send_text_callback, lambda c: c.data == 'send_text')
    dp.callback_query.register(callback.send_audio_callback, lambda c: c.data == 'send_audio')
    dp.callback_query.register(callback.query_expenses_callback, lambda c: c.data == 'query_expenses')

    # Регистрация обработчиков для кнопок "Да" и "Нет"
    dp.callback_query.register(confirm_handler.handle_confirm_yes, F.data == "confirm_yes")
    dp.callback_query.register(confirm_handler.handle_confirm_no, F.data == "confirm_no")

    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())
