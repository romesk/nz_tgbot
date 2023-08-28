from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.base import BaseDAO
from src.database.models import Action, User


class ActionDAO(BaseDAO[Action]):
    def __init__(self, session: AsyncSession):
        super().__init__(Action, session)

    async def create(self, chat_id: int, student_id: int, action: str) -> Action:
        action = await self.session.merge(
            Action(user_id=chat_id, student_id=student_id, action=action)
        )
        await self.commit()
        return action

    async def get_last_action(self, chat_id: int, action: str) -> Action:
        """
        Returns the last action of a student connected to user by action type
        """

        user = await self.session.execute(select(User).where(User.id == chat_id))

        results = await self.session.execute(
            select(Action)
            .where(and_(Action.student_id == user.student_id, Action.action == action))
            .order_by(Action.time_created.desc())
            .limit(1)
        )

        return results.scalars().first()
