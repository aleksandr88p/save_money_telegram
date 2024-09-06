from aiogram.fsm.state import StatesGroup, State

class AudioState(StatesGroup):
    waiting_for_audio_expenses = State()  # Состояние ожидания аудио для трат


class TextState(StatesGroup):
    waiting_for_text = State()  # Состояние ожидания текста от пользователя