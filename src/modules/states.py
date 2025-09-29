from aiogram.dispatcher.filters.state import State, StatesGroup

class ClientStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_notes = State()
