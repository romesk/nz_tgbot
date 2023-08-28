from aiogram import types
from aiogram.dispatcher import FSMContext

from src import states
from src.keyboards import generate_login_kb, generate_main_kb
from src.database.dao.holder import DAO
from src.texts import TEXTS
from src.models import NzUaAPI
from src.utils import logger


async def bot_start(message: types.Message, dao: DAO):
    logger.info(f"Bot started by user. {message}")
    await message.answer(TEXTS.START.HELLO, reply_markup=await generate_login_kb(btn_text=TEXTS.START.LOGIN_BTN))
    await dao.user.create(message.chat.id, message.from_user.full_name, message.from_user.username)


async def ask_username(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer(TEXTS.START.ASK_LOGIN)

    await states.EnterLoginData.username.set()


async def ask_password(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)

    await message.answer(TEXTS.START.ASK_PASSWORD)
    await states.EnterLoginData.next()


async def finish_login(message: types.Message, state: FSMContext, dao: DAO):

    password = message.text
    async with state.proxy() as data:
        username = data.get("username")

    nz_ua = NzUaAPI()
    auth_response = await nz_ua.authentificate(username, password)
    logger.info(f"User authentificate: {message.from_user}\nAuth response: {auth_response}")

    err_msg = auth_response['error_message']

    user_fullname = auth_response.get('FIO', "")
    student_id = auth_response.get('student_id', "")
    access_token = auth_response.get('access_token', f"FAIL: {err_msg}")

    if not err_msg:
        await message.answer(TEXTS.START.LOGIN_SUCCESS)
        await message.answer(TEXTS.START.WELCOME.format(name=user_fullname),
                             reply_markup=await generate_main_kb())
    else:
        await message.answer(TEXTS.START.LOGIN_FAIL.format(err_msg=err_msg),
                             reply_markup=await generate_login_kb(btn_text=TEXTS.START.RETRY_LOGIN))
        logger.warning(f"User login failed: {message.from_user}\nAuth response: {auth_response}")

    await dao.user.create(
        message.chat.id,
        message.from_user.full_name,
        message.from_user.username,
        username,
        password,
        access_token,
        user_fullname,
        student_id
    )

    await state.finish()
