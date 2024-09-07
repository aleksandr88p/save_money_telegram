from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

from core.keyboards.inline import get_russian_keyboard, get_english_keyboard
from utils.helper import get_user_language
from core.keyboards.reply_keyboard import get_main_keyboard



async def show_keyboard(message: Message):
    user_id = message.from_user.id
    language = get_user_language(user_id)
    # Показываем клавиатуру без отправки сообщения
    if language == 'english':
        keyboard = get_english_keyboard()
    else:
        keyboard = get_russian_keyboard()

    await message.answer("Here is the keyboard:", reply_markup=keyboard)


async def send_welcome(message: Message):
    user_id = message.from_user.id
    main_keyboard = get_main_keyboard()

    # Отправляем сообщение с клавиатурой
    await message.answer("Welcome!", reply_markup=main_keyboard)





async def get_help(message: Message):
    user_id = message.from_user.id
    language = get_user_language(user_id)

    if language == 'english':
        help_text = (
            "/start - Start the bot\n"
            "/help - Show the list of commands\n"
            "/query - Request expense information\n"
            "/audio - Send an audio message about your expenses\n"
            "/submit - Send text for analysis and saving"
        )
        await message.answer(help_text)
    else:
        help_text = (
            "/start - Запустить бота\n"
            "/help - Показать список команд\n"
            "/query - Запросить информацию о расходах\n"
            "/audio - Отправить аудио сообщение о твоих покупках\n"
            "/submit - Отправить текст для анализа и сохранения"
        )
        await message.answer(help_text)
