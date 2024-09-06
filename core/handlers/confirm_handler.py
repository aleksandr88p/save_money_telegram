from aiogram import types
from aiogram.types import CallbackQuery
from utils.helper import get_user_language
import aiohttp
from bot.config import Config


# Обработчик для нажатия "Да"
async def handle_confirm_yes(callback: CallbackQuery):
    user_id = callback.from_user.id
    language = get_user_language(user_id)

    # Отправляем запрос на API для подтверждения
    headers = {"Authorization": Config.API_KEY}

    # Формируем URL с параметрами user_id и confirmation
    url = f"{Config.API_URL}/confirm-text/?user_id={user_id}&confirmation=true"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                if language == 'english':
                    await callback.message.answer("Text confirmed and saved to the database.")
                else:
                    await callback.message.answer("Текст подтвержден и сохранен в базе данных.")
            else:
                if language == 'english':
                    await callback.message.answer(f"An error occurred while confirming the text: {response.status}")
                else:
                    await callback.message.answer(f"Произошла ошибка при подтверждении текста: {response.status}")

    # Удаляем клавиатуру после нажатия
    await callback.message.edit_reply_markup(reply_markup=None)


# Обработчик для нажатия "Нет"
async def handle_confirm_no(callback: CallbackQuery):
    user_id = callback.from_user.id
    language = get_user_language(user_id)

    # Отправляем запрос на API для отмены
    headers = {"Authorization": Config.API_KEY}

    # Формируем URL с параметрами user_id и confirmation
    url = f"{Config.API_URL}/confirm-text/?user_id={user_id}&confirmation=false"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                if language == 'english':
                    await callback.message.answer("Text declined and removed from temporary storage.")
                else:
                    await callback.message.answer("Текст отклонен и удален из временного хранилища.")
            else:
                if language == 'english':
                    await callback.message.answer(f"An error occurred while declining the text: {response.status}")
                else:
                    await callback.message.answer(f"Произошла ошибка при отклонении текста: {response.status}")

    # Удаляем клавиатуру после нажатия
    await callback.message.edit_reply_markup(reply_markup=None)
