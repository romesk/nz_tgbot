from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.user import UserDAO
from src.database.dao.mark import MarkDAO
from src.database.dao.action import ActionDAO


class DAO:
    """Holder data access object"""
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    def user(self):
        return UserDAO(self.session)

    @property
    def mark(self):
        return MarkDAO(self.session)

    @property
    def action(self):
        return ActionDAO(self.session)
