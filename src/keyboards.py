from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_login_kb(btn_text: str) -> InlineKeyboardMarkup:
    """
    Generates keyboard with username button
    """

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text=f"{btn_text} 👀", callback_data="login"))

    return kb
