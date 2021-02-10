from aiogram.dispatcher.filters.state import StatesGroup, State


class Info(StatesGroup):
    login = State()
    password = State()
    user_id = State()


class Support(StatesGroup):
    name = State()
    text = State()