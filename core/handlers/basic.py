from aiogram.types import Message, ReplyKeyboardRemove
from core.keyboards.inline import get_russian_keyboard, get_english_keyboard
from utils.helper import get_user_language

async def send_welcome(message: Message):
    user_id = message.from_user.id
    language = get_user_language(user_id)

    # Отображаем сообщение и клавиатуру в зависимости от языка
    if language == 'english':
        keyboard = get_english_keyboard()
        await message.answer("Welcome to the Expense Tracker Bot!", reply_markup=keyboard)
    else:
        keyboard = get_russian_keyboard()
        await message.answer("Добро пожаловать в бот учета расходов!", reply_markup=keyboard)





async def get_help(message: Message):
    user_id = message.from_user.id
    language = get_user_language(user_id)

    if language == 'english':
        help_text = (
            "/start - Start the bot\n"
            "/help - Show the list of commands\n"
            "/query - Request expense information\n"
            "/confirm - Confirm the text\n"
            "/audio - Send an audio file to convert to text\n"
            "/submit - Send text for analysis and saving"
        )
        await message.answer(help_text)
    else:
        help_text = (
            "/start - Запустить бота\n"
            "/help - Показать список команд\n"
            "/query - Запросить информацию о расходах\n"
            "/confirm - Подтвердить текст\n"
            "/audio - Отправить аудио для преобразования в текст\n"
            "/submit - Отправить текст для анализа и сохранения"
        )
        await message.answer(help_text)
