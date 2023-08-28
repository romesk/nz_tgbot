from aiogram import Dispatcher

from src import states
from src.handlers import start, show_diary, show_grades
from src.keyboards import week_callback_data, day_callback_data, change_week_callback_data, subject_cb


def register_commands(dp: Dispatcher):

    dp.register_message_handler(start.bot_start, commands="start")

    # Register log in handlers
    dp.register_callback_query_handler(start.ask_username, text="login")
    dp.register_message_handler(start.ask_password, state=states.EnterLoginData.username)
    dp.register_message_handler(start.finish_login, state=states.EnterLoginData.password)

    # Register show diary handlers
    dp.register_message_handler(show_diary.ask_diary_week, text="Щоденник 🗒️")
    dp.register_message_handler(show_diary.ask_diary_week, commands="diary")

    dp.register_callback_query_handler(show_diary.ask_diary_week_day, week_callback_data.filter())
    dp.register_callback_query_handler(show_diary.show_diary, day_callback_data.filter())
    dp.register_callback_query_handler(show_diary.change_diary_week, change_week_callback_data.filter())

    # Register show grades handlers
    dp.register_message_handler(show_grades.ask_subject, text="Оцінки 📝", state="*")
    dp.register_message_handler(show_grades.ask_subject, commands="grades", state="*")

    dp.register_callback_query_handler(show_grades.show_grades, subject_cb.filter(), state="Subjects:subject")
