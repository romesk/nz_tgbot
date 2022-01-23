from aiogram.types import Message

from src.services.db.models import User


async def add_user(message: Message, login: str = None, password: str = None, access_token: str = None):
    sessionmaker = message.bot.get('db')

    async with sessionmaker() as session:
        await session.merge(
            User(user_id=message.from_user.id, fullname=message.from_user.full_name,
                 username=message.from_user.username, login=login, password=password,
                 access_token=access_token)
        )
        await session.commit()
