import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


# callback datas used in keyboards
week_callback_data = CallbackData("week", "name", "week_start", "week_end")
day_callback_data = CallbackData("day", "day_number", "date", "week_start", "week_end")
change_week_callback_data = CallbackData("change_week", "name", "week_start", "week_end")
subject_cb = CallbackData("subject", "name")


async def generate_login_kb(btn_text: str) -> InlineKeyboardMarkup:
    """
    Generates keyboard with username button
    """

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text=f"{btn_text} 👀", callback_data="login"))

    return kb


async def generate_main_kb() -> ReplyKeyboardMarkup:
    """
    Generates main keyboard
    """

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Щоденник 🗒️", "Оцінки 📝")

    return kb


async def generate_week_kb() -> InlineKeyboardMarkup:
    """
    Generates keyboard with weeks. Includes current week, previous and next
    """

    kb = InlineKeyboardMarkup()

    current_week_start = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday())
    current_week_end = current_week_start + datetime.timedelta(days=6)

    previous_week_start = current_week_start - datetime.timedelta(days=7)
    previous_week_end = previous_week_start + datetime.timedelta(days=6)

    next_week_start = current_week_start + datetime.timedelta(days=7)
    next_week_end = next_week_start + datetime.timedelta(days=6)

    kb.add(
        InlineKeyboardButton(
            text=f"{previous_week_start.strftime('%d.%m')} - {previous_week_end.strftime('%d.%m')}",
            callback_data=week_callback_data.new(name="prev_week",
                                                 week_start=previous_week_start.strftime("%Y-%m-%d"),
                                                 week_end=previous_week_end.strftime("%Y-%m-%d"))
        )
    )

    kb.add(
        InlineKeyboardButton(
            text=f"➡️ {current_week_start.strftime('%d.%m')} - {current_week_end.strftime('%d.%m')} ⬅️",
            callback_data=week_callback_data.new(name="current_week",
                                                 week_start=current_week_start.strftime("%Y-%m-%d"),
                                                 week_end=current_week_end.strftime("%Y-%m-%d"))
        )
    )

    kb.add(
        InlineKeyboardButton(
            text=f"{next_week_start.strftime('%d.%m')} - {next_week_end.strftime('%d.%m')}",
            callback_data=week_callback_data.new(name="next_week",
                                                 week_start=next_week_start.strftime("%Y-%m-%d"),
                                                 week_end=next_week_end.strftime("%Y-%m-%d"))
        )
    )

    return kb


async def generate_week_days_kb(week_start: str, week_end: str) -> InlineKeyboardMarkup:
    """
    Generates keyboard with days of week
    """

    kb = InlineKeyboardMarkup()

    start = datetime.datetime.strptime(week_start, "%Y-%m-%d")
    end = datetime.datetime.strptime(week_end, "%Y-%m-%d")

    day_names = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд")
    dates = [date.strftime("%d.%m") for date in (start + datetime.timedelta(n) for n in range((end - start).days + 1))]
    today_str = datetime.datetime.today().strftime("%d.%m")

    for day_name, date in zip(day_names, dates):
        kb.insert(
            InlineKeyboardButton(
                text=f"{day_name} - {date}" if date != today_str else f"🔘 {day_name} - {date}",
                callback_data=day_callback_data.new(
                    day_number=day_names.index(day_name) + 1,
                    date=datetime.datetime.strptime(date, "%d.%m").strftime(f"{start.year}-%m-%d"),
                    week_start=week_start,
                    week_end=week_end
                )
            )
        )

    kb.insert(
        InlineKeyboardButton(
            text="Весь Тиждень",
            callback_data=day_callback_data.new(day_number=-1,
                                                date="all_week",
                                                week_start=week_start,
                                                week_end=week_end)
        )
    )

    kb.add(
        InlineKeyboardButton(
            text="⬅️ Попередній",
            callback_data=change_week_callback_data.new(
                name="previous_week",
                week_start=start.strftime("%Y-%m-%d"),
                week_end=end.strftime("%Y-%m-%d")
            )
        ),
        InlineKeyboardButton(
            text="Наступний ➡️",
            callback_data=change_week_callback_data.new(
                name="next_week",
                week_start=start.strftime("%Y-%m-%d"),
                week_end=end.strftime("%Y-%m-%d")
            )
        )
    )

    return kb


async def generate_subjects_kb(subjects: list) -> InlineKeyboardMarkup:
    """
    Generates keyboard with subjects
    """

    kb = InlineKeyboardMarkup()

    subjects.insert(0, "Всі предмети")

    for subject in subjects:
        kb.add(InlineKeyboardButton(text=subject, callback_data=subject_cb.new(name=subject)))

    return kb
