from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMIN_ID
from loader import dp
from states.states import Support
from utils.misc import rate_limit


@dp.message_handler(commands="support")
@rate_limit(600, "support")
async def support(message: types.Message):
    await message.answer('Будь ласка, напишіть ваші скарги, пропозиції та побажання. '
                         'Ми обов\'зково приймемо це до уваги.')
    await message.answer('Введіть ваш нікнейм в Telegram (@sample) для зворотнього зв\'язку'
                         'або надішліть будь-який символ, якщо бажаєте залишитись анонімним.')
    await Support.name.set()


@dp.message_handler(state=Support.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введіть текст повідомлення..')
    await Support.next()


@dp.message_handler(state=Support.text)
async def process_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.finish()
    await message.answer('Дякуємо за Ваше звернення!')
    name = data['name']
    text = data['text']
    msg_text = ['<b>[Support message]</b>\n',
                f'<b>Name:</b> {name}',
                f'<b>TG:</b> @{message.from_user.username}',
                f'<b>Message text:</b>\n{text}']
    await dp.bot.send_message(ADMIN_ID, '\n'.join(msg_text))