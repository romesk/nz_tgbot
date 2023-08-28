import asyncio
import logging
from typing import Callable

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from src import config
from src import handlers
from src.middlewares.database import DatabaseMiddleware
from src.database.models import Base
from src.utils import logger


async def main():

    logger.info("Bot started!")
    logger.debug("Debug mode is on!")

    engine: AsyncEngine = create_async_engine(config.POSTGRES_URI, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker: Callable = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    dp.middleware.setup(DatabaseMiddleware(async_sessionmaker))

    handlers.register_commands(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
