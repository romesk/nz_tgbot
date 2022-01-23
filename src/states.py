from aiogram.dispatcher.filters.state import StatesGroup, State


class EnterLoginData(StatesGroup):
    username = State()
    password = State()
