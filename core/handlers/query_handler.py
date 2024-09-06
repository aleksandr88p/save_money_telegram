from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.helper import get_user_language
import aiohttp
from bot.config import Config
from core.states import QueryState




# Обработчик команды /query
async def handle_query_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_user_language(user_id)

    # Сохраняем состояние ожидания запроса
    await state.set_state(QueryState.waiting_for_query)

    # Сообщаем пользователю, что бот ожидает запрос
    if language == 'english':
        await message.answer("Please enter the query you would like to execute.")
    else:
        await message.answer("Пожалуйста, введите запрос, который вы хотите выполнить.")

# Обработчик текста запроса
async def handle_query_submission(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_user_language(user_id)

    # Проверяем, находимся ли мы в состоянии ожидания запроса
    if await state.get_state() == QueryState.waiting_for_query:
        user_query = message.text  # Текст запроса от пользователя

        # Отправляем запрос на API
        url = f"{Config.API_URL}/query-expenses/"
        headers = {"Authorization": Config.API_KEY}
        params = {"user_telegram_id": user_id, "query": user_query}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, params=params) as response:
                if response.status == 200:
                    result = await response.json()
                    if language == 'english':
                        await message.answer(f"Here: {result['response']}")
                    else:
                        await message.answer(f"Вот: {result['response']}")
                else:
                    if language == 'english':
                        await message.answer(f"An error occurred while processing your query: {response.status}")
                    else:
                        await message.answer(f"Произошла ошибка при обработке вашего запроса: {response.status}")

        # Очищаем состояние после обработки запроса
        await state.clear()