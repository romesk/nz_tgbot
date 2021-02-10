import logging

from aiogram import Dispatcher

from data.config import ADMIN_ID


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(ADMIN_ID, "[Admin msg] Bot launched")
    except Exception as err:
        logging.exception(err)
