from asyncpg import UniqueViolationError

from utils.db_api.schemas.user import User


async def add_user(user_id: int, login: str, password: str):
    """
    Записывает данные или обновляет их
    """
    try:
        user = User(user_id=user_id, login=login, password=password)
        await user.create()
    except UniqueViolationError:
        user = User(user_id=user_id, login=login, password=password)
        await user.update(user_id=user_id, login=login, password=password).apply()


async def get_info(user_id: int):
    """
    Достает логин и пароль
    """
    user = await User.get(user_id)
    login = user.login
    password = user.password
    return login, password


async def get_all_users():
    """
    Достает все записи из базы
    """
    users = await User.query.gino.all()
    return users


async def update_news_number(user_id: int, news: int):
    """
    Обновление значения news
    """
    user = User(user_id=user_id)
    await user.update(news=news).apply()


