from aiogram.types import Message
from sqlalchemy import and_, select

from src.services.db.models import User, Marks


async def add_user(
    message: Message, login: str = None, password: str = None, access_token: str = None
):
    sessionmaker = message.bot.get("db")

    async with sessionmaker() as session:
        await session.merge(
            User(
                user_id=message.from_user.id,
                fullname=message.from_user.full_name,
                username=message.from_user.username,
                login=login,
                password=password,
                access_token=access_token,
            )
        )
        await session.commit()


async def get_user_bearer_token(message: Message) -> str:
    sessionmaker = message.bot.get("db")

    async with sessionmaker() as session:
        user = await session.get(User, message.chat.id)
        return user.access_token


async def add_mark(message: Message, subject: str, subject_id: int, mark: int):
    sessionmaker = message.bot.get("db")

    async with sessionmaker() as session:
        await session.merge(
            Marks(
                user_id=message.chat.id,
                subject=subject,
                subject_id=subject_id,
                mark=mark,
            )
        )
        await session.commit()


async def get_marks(message: Message, subject_id: int) -> list:
    sessionmaker = message.bot.get("db")
    print(subject_id)

    async with sessionmaker() as session:
        results = await session.execute(
            select(Marks).where(
                and_(
                    Marks.user_id == message.chat.id,
                    Marks.subject_id == int(subject_id),
                )
            )
        )

        return [result.mark for result in results]
