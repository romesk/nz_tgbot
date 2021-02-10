from loader import dp, pn, aiosched
from utils.db_api import db_commands


@aiosched.scheduled_job('interval', seconds=60)
async def check():
    async for user in get_users():
        ex_news = int(user.news)  # кол-во новостей сохраненных в бд
        news_number = await get_news(user)  # кол-во новостей из сайта
        if news_number is None and ex_news != 0:
            await db_commands.update_news_number(user.user_id, 0)
        if news_number is not None and news_number != ex_news:
            await db_commands.update_news_number(user.user_id, news=news_number)  # обновление значения в бд
            delta = news_number-ex_news
            await send_msg(user.user_id, news_number, delta)


async def get_users():
    users = await db_commands.get_all_users()
    for user in users:
        yield user


async def get_news(user):
    return await pn().check_new(user.login, user.password)


async def send_msg(user_id, news, delta):
    await dp.bot.send_message(user_id, f'📢 Нових записів: {news}(+{delta})')


async def start_checker(dp):
    aiosched.start()
