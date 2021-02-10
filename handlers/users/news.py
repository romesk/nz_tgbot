from aiogram import types

from loader import dp, pn
from utils.misc import rate_limit
from utils.db_api import db_commands


@dp.message_handler(text='Новини')
@dp.message_handler(commands='news')
@rate_limit(10, 'Новини')
@rate_limit(10, 'news')
async def show_news(message: types.Message):
    msg = await message.answer('⌛ Виконується обробка запиту..')
    # парсит новости с сайта
    info = await db_commands.get_info(message.from_user.id)  # ('login', 'password')
    data = await pn().get_news(info[0], info[1])
    await msg.edit_text(data)
