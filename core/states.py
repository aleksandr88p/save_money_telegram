from aiogram.fsm.state import StatesGroup, State

class AudioState(StatesGroup):
    waiting_for_audio_expenses = State()  # Состояние ожидания аудио для трат


class TextState(StatesGroup):
    waiting_for_text = State()  # Состояние ожидания текста с тратами от пользователя


class QueryState(StatesGroup):
    waiting_for_query = State()  # Состояние ожидания запроса для sql агента от пользователя
