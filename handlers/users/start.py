from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp, kb, pn
from states.states import Info
from utils.misc import rate_limit
from utils.db_api import db_commands


@dp.message_handler(CommandStart())
@rate_limit(10)
async def bot_start(message: types.Message):
    await message.answer('Увійдіть у свій кабінет на сайті nz.ua')
    await message.answer('Введіть свій логін')
    await Info.login.set()


@dp.message_handler(state=Info.login)
async def process_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введіть свій пароль")
    await Info.next()


@dp.message_handler(state=Info.password)
async def process_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    user_data = await state.get_data()
    data = await pn().get_news(user_data['login'], user_data['password'])  # парсит новости используя данные из state
    await db_commands.add_user(message.from_user.id, user_data['login'], user_data['password'])
    await dp.bot.send_message(message.from_user.id, data,
                              reply_markup=kb.news_kb)
    await state.finish()
