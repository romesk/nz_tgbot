from aiogram import types
from aiogram.dispatcher import FSMContext

from src import states
from src.services import api_calls
from src.keyboards import generate_login_kb
from src.services.db import db_calls


async def bot_start(message: types.Message):
    welcome_msg = "👋 Вітаю у боті NzUa. Головна ціль - зробити зручного Телеграм помічника, " \
                  "щоб користуватись основними функціями nz.ua у твоєму улюбленому месенджері 🤩 То ж не зволікай і " \
                  "тисни на кнопку нижче! 😎"

    await message.answer(welcome_msg, reply_markup=await generate_login_kb(btn_text="Увійти в аккаунт"))


async def ask_username(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Введи свій логін 🧐")

    await states.EnterLoginData.username.set()


async def ask_password(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)

    await message.answer("Введи свій пароль 🔐")
    await states.EnterLoginData.next()


async def finish_login(message: types.Message, state: FSMContext):

    password = message.text
    async with state.proxy() as data:
        username = data.get("username")

    auth_response = await api_calls.authentificate(username, password)

    err_msg = auth_response['error_message']

    if not err_msg:
        access_token = auth_response['access_token']
        await message.answer(f"Виконано успішний вхід 🔓\n<i>Щоб зберегти дані для входу у безпеці, ти можеш видалити "
                             f"їх з переписки </i>")
        await message.answer(f"Ласкаво просимо, {auth_response['FIO']} 😁")

        await db_calls.add_user(message=message, login=username, password=password, access_token=access_token)

    else:
        await message.answer(f"{err_msg} 🙁", reply_markup=await generate_login_kb(btn_text="Спробувати ще раз"))
        await db_calls.add_user(message=message)

    await state.finish()
