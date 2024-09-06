from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utils.helper import get_user_language
import aiohttp
from bot.config import Config
from core.states import TextState  # Подключаем наше состояние


# Обработчик для получения текста от пользователя
async def handle_text_submission(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_user_language(user_id)

    # Проверяем, находимся ли мы в состоянии ожидания текста
    if await state.get_state() == TextState.waiting_for_text:
    # if await state.get_state() == TextState.waiting_for_text.state:
        # Получаем введённый пользователем текст
        user_text = message.text

        headers = {"Authorization": Config.API_KEY}

        # Отправляем текст на API для анализа и сохранения
        async with aiohttp.ClientSession() as session:
            params = {'user_id': user_id, 'text': user_text}
            async with session.post(f"{Config.API_URL}/submit-text/", headers=headers, params=params) as response:

                if response.status == 200:
                    if language == 'english':
                        await message.answer("Text submitted successfully and saved to the database.")
                    else:
                        await message.answer("Текст успешно отправлен и сохранен в базе данных.")
                else:
                    if language == 'english':
                        await message.answer(f"An error occurred while submitting the text: {response.status}")
                    else:
                        await message.answer(f"Произошла ошибка при отправке текста: {response.status}")

        # Очищаем состояние после отправки текста
        await state.clear()


# Обработчик команды /submit
async def handle_submit_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_user_language(user_id)

    # Сохраняем состояние ожидания текста от пользователя
    await state.set_state(TextState.waiting_for_text)

    # Отправляем сообщение пользователю, что бот ожидает текст
    if language == 'english':
        await message.answer("Please send the text you want to submit.")
    else:
        await message.answer("Пожалуйста, отправьте текст, который вы хотите отправить.")
