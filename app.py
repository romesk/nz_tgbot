import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src import config
from src.handlers import register_commands
from src.services.db import base


async def main():

    logging.basicConfig(
        format=u'[%(asctime)s] %(filename)s [LINE:%(lineno)d] #%(levelname)-8s  %(message)s',
        level=logging.INFO
    )

    engine = await base.async_main()
    async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    bot["db"] = async_sessionmaker

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    register_commands(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
