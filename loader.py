from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config
from keyboards.default import keyboards
from utils.db_api.postgresql import db
from utils.news_parser import ParseNews

bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
kb = keyboards
pn = ParseNews
aiosched = AsyncIOScheduler()

__all__ = ['bot', 'storage', 'dp', 'kb', 'pn', 'aiosched', 'db']
