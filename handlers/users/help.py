from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit


@dp.message_handler(CommandHelp())
@rate_limit(5, 'help')
async def bot_help(message: types.Message):
    text = [
        '<b>Список команд:</b>\n ',
        '📲 /start - Вхід на сайт.',
        '📲 /help - Отримати справку по командах.',
        '📲 /news - Показати останні записи',
        '📲 /support - Зворотній зв\'язок. (Увага! Можливо звернутись лише раз в 10 хвилин)'
    ]
    await message.answer('\n'.join(text))
