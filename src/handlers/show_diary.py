import asyncio
import datetime
from datetime import timedelta

from aiogram.types import Message, CallbackQuery

from src.models import Diary
from src.keyboards import generate_week_kb, generate_week_days_kb
from src.models import NzUaAPI
from src.texts import TEXTS
from src.database.dao import DAO
from src.utils import logger


async def ask_diary_week(message: Message):
    """
    Asks user which week to show. Possible options are previous, current and next week
    """

    await message.answer(TEXTS.DIARY.ASK_WEEK, reply_markup=await generate_week_kb())


async def ask_diary_week_day(call: CallbackQuery, callback_data: dict):
    """
    Asks user which day of the week to show
    """

    await call.message.delete()
    await call.message.answer(TEXTS.DIARY.ASK_WEEK_DAY,
                              reply_markup=await generate_week_days_kb(callback_data['week_start'],
                                                                       callback_data['week_end']))


async def show_diary(call: CallbackQuery, callback_data: dict, dao: DAO):
    """
    Sends user his diary for selected parameters
    """

    await call.message.delete()
    await call.message.answer(TEXTS.DIARY.LOADING)

    user = await dao.user.get_by_id(call.from_user.id)
    nz_ua = NzUaAPI(user.access_token)
    diary_json = await nz_ua.get_diary(callback_data['week_start'], callback_data['week_end'])
    logger.info(f"Diary for {call.from_user.id} loaded. {diary_json}")

    diary = Diary(diary_json)

    if callback_data['date'] == 'all_week':
        start = datetime.datetime.strptime(callback_data['week_start'], '%Y-%m-%d')
        end = datetime.datetime.strptime(callback_data['week_end'], '%Y-%m-%d')

        dates = [date.strftime("%Y-%m-%d") for date in
                 (start + timedelta(n) for n in range((end - start).days + 1))]

        for date in dates:
            await call.message.answer(await diary.get_diary_for_day(date))
            await asyncio.sleep(0.5)
    else:
        await call.message.answer(await diary.get_diary_for_day(callback_data['date']))


async def change_diary_week(call: CallbackQuery, callback_data: dict):
    """
    Changes week inline keyboard to show
    """

    start = datetime.datetime.strptime(callback_data['week_start'], '%Y-%m-%d')
    end = datetime.datetime.strptime(callback_data['week_end'], '%Y-%m-%d')

    if callback_data['name'] == 'previous_week':
        start -= timedelta(days=7)
        end -= timedelta(days=7)
    elif callback_data['name'] == 'next_week':
        start += timedelta(days=7)
        end += timedelta(days=7)

    await call.message.edit_reply_markup(
        reply_markup=await generate_week_days_kb(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    )
