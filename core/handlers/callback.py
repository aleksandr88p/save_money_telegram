from aiogram.types import CallbackQuery
from utils.helper import set_user_language
from core.keyboards.inline import get_russian_keyboard, get_english_keyboard

async def switch_to_russian(call: CallbackQuery):
    set_user_language(call.from_user.id, 'russian')
    keyboard = get_russian_keyboard()
    await call.message.answer("Язык изменен на русский.", reply_markup=keyboard)
    await call.answer()

async def switch_to_english(call: CallbackQuery):
    set_user_language(call.from_user.id, 'english')
    keyboard = get_english_keyboard()
    await call.message.answer("Language switched to English.", reply_markup=keyboard)
    await call.answer()