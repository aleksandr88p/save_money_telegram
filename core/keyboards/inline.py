from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для русского языка
def get_russian_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отправить текст", callback_data="send_text")],
        [InlineKeyboardButton(text="Отправить аудио", callback_data="send_audio")],
        [InlineKeyboardButton(text="Переключить на English", callback_data="switch_to_english")]
    ])
    return keyboard

# Клавиатура для английского языка
def get_english_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Send Text", callback_data="send_text")],
        [InlineKeyboardButton(text="Send Audio", callback_data="send_audio")],
        [InlineKeyboardButton(text="Switch to Russian", callback_data="switch_to_russian")]
    ])
    return keyboard
