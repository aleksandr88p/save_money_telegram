import aiohttp

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core.keyboards.inline import get_russian_keyboard, get_english_keyboard, get_confirm_keyboard
from utils.helper import get_user_language
from bot.config import Config
from core.states import AudioState



async def audio_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_user_language(user_id)

    # Устанавливаем состояние ожидания аудио для трат
    await state.set_state(AudioState.waiting_for_audio_expenses)

    if language == 'english':
        await message.answer("Please send an audio message describing your expenses.")
    else:
        await message.answer("Пожалуйста, отправьте аудиосообщение с описанием ваших расходов.")



async def handle_voice(message: Message, state: FSMContext):
    # Проверяем, находимся ли мы в состоянии ожидания аудио для трат
    if await state.get_state() != AudioState.waiting_for_audio_expenses:
        # Если пользователь не вызвал команду /audio перед отправкой голосового сообщения
        await message.answer("Unexpected audio message. Please use the /audio command first.")
        return

    user_id = message.from_user.id
    language = get_user_language(user_id)

    # Уведомляем пользователя о начале обработки
    if language == 'english':
        await message.answer("Your audio is being processed, please wait...")
    else:
        await message.answer("Ваше аудио обрабатывается, пожалуйста, подождите...")


    try:
        # Получаем файл с Telegram сервера
        file_info = await message.bot.get_file(message.voice.file_id)
        file_path = file_info.file_path
        file = await message.bot.download_file(file_path)

        # Подготовка файла и отправка на API
        files = {'file': file}
        headers = {"Authorization": Config.API_KEY}  # Используем Bearer Token

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{Config.API_URL}/audio-to-text/?user_id={user_id}", headers=headers, data=files) as response:
                if response.status == 200:
                    result = await response.json()
                    recognized_text = result.get("recognized_text")

                    # Отправляем текст пользователю для подтверждения
                    if language == 'english':
                        await message.answer(f"Recognized text: {recognized_text}\nDo you confirm this text?", reply_markup=get_confirm_keyboard(language))
                    else:
                        await message.answer(f"Распознанный текст: {recognized_text}\nПодтверждаете этот текст?", reply_markup=get_confirm_keyboard(language))
                else:
                    # Если API вернул ошибку
                    if language == 'english':
                        await message.answer("An error occurred while processing the audio.")
                    else:
                        await message.answer("Произошла ошибка при обработке аудио.")
    except Exception as e:
        # Логирование ошибки для отладки
        print(f"Error processing audio: {str(e)}")

        # Уведомление пользователя о проблеме
        if language == 'english':
            await message.answer("An error occurred while processing the audio.")
        else:
            await message.answer("Произошла ошибка при обработке аудио.")
    finally:
        # Очищаем состояние, завершаем обработку
        await state.clear()