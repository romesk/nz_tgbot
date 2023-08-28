from aiogram.dispatcher.filters.state import StatesGroup, State


class EnterLoginData(StatesGroup):
    username = State()
    password = State()


class Subjects(StatesGroup):
    subject = State()
