from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Help"), KeyboardButton(text="Show Keyboard")]
    ], resize_keyboard=True)