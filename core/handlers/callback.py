from aiogram.types import CallbackQuery
from aiogram import types
from aiogram.fsm.context import FSMContext
from core.states import TextState, AudioState, QueryState
from core.handlers import submit_handler, audio_handler
from utils.helper import get_user_language, set_user_language
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



async def send_text_callback(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    language = get_user_language(user_id)

    # Устанавливаем состояние ожидания текста
    await state.set_state(TextState.waiting_for_text)

    # Сообщаем пользователю, что бот ожидает текст
    if language == 'english':
        await call.message.answer("Please send the text you want to submit.")
    else:
        await call.message.answer("Пожалуйста, отправьте текст, который вы хотите отправить.")

    await call.answer()


async def send_audio_callback(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    language = get_user_language(user_id)

    # Устанавливаем состояние ожидания аудио
    await state.set_state(AudioState.waiting_for_audio_expenses)

    # Сообщаем пользователю, что бот ожидает аудио
    if language == 'english':
        await call.message.answer("Please send an audio message describing your expenses.")
    else:
        await call.message.answer("Пожалуйста, отправьте аудиосообщение с описанием ваших расходов.")

    await call.answer()


async def query_expenses_callback(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    language = get_user_language(user_id)

    # Устанавливаем состояние ожидания запроса расходов
    await state.set_state(QueryState.waiting_for_query)

    # Сообщаем пользователю, что бот ожидает запрос
    if language == 'english':
        await call.message.answer("Please enter the query you would like to execute.")
    else:
        await call.message.answer("Пожалуйста, введите запрос, который вы хотите выполнить.")

    await call.answer()