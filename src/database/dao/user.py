from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.base import BaseDAO
from src.database.models import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def create(
        self,
        chat_id: int,
        fullname: str,
        username: str,
        login: str = None,
        password: str = None,
        access_token: str = None,
        fullname_nzua: str = None,
        student_id: int = None
    ) -> User:
        user = await self.session.merge(
            User(
                id=chat_id,
                fullname=fullname,
                username=username,
                login=login,
                password=password,
                access_token=access_token,
                fullname_nzua=fullname_nzua,
                student_id=student_id
            )
        )
        await self.commit()
        return user
