from aiogram.types import Message

async def send_welcome(message: Message):
    """
    Обработчик команды /start.
    """
    await message.answer("Welcome to the Expense Tracker Bot!")


from aiogram.types import Message

async def send_welcome(message: Message):
    """
    Обработчик команды /start.
    """
    await message.answer("Welcome to the Expense Tracker Bot!")

async def get_help(message: Message):
    """
    Обработчик команды /help.
    Показывает список доступных команд.
    """
    help_text = (
        "/start - Запустить бота\n"
        "/help - Показать список команд\n"
        "/query - Запросить информацию о расходах\n"
        "/confirm - Подтвердить текст\n"
        "/audio - Отправить аудио для преобразования в текст\n"
        "/submit - Отправить текст для анализа и сохранения"
    )
    await message.answer(help_text)
