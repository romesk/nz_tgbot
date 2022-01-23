from aiogram import Dispatcher

from src import states
from src.handlers import start


def register_commands(dp: Dispatcher):

    dp.register_message_handler(start.bot_start, commands="start")

    # Register log in handlers
    dp.register_callback_query_handler(start.ask_username, text="login")
    dp.register_message_handler(start.ask_password, state=states.EnterLoginData.username)
    dp.register_message_handler(start.finish_login, state=states.EnterLoginData.password)
