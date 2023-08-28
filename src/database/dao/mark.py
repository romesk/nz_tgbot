from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.base import BaseDAO
from src.database.models import Mark


class MarkDAO(BaseDAO[Mark]):
    def __init__(self, session: AsyncSession):
        super().__init__(Mark, session)

    async def create(
        self,
        chat_id: int,
        student_id: int,
        subject_name: str,
        subject_id: int,
        mark: int,
        lesson_date: datetime,
        lesson_type: str,
        comment: str,
        lesson_id: int
    ) -> Mark:
        mark = await self.session.merge(
            Mark(
                user_id=chat_id,
                student_id=student_id,
                subject=subject_name,
                subject_id=subject_id,
                mark=mark,
                lesson_date=lesson_date,
                lesson_type=lesson_type,
                comment=comment,
                lesson_id=lesson_id
            )
        )
        await self.commit()
        return mark

    async def get_marks_for_subject(self, student_id: int, subject_id: int) -> list[Mark]:

        results = await self.session.execute(
            select(Mark).where(and_(Mark.student_id == student_id, Mark.subject_id == subject_id))
        )

        return results.scalars().all()

    async def delete(self, student_id: int, lesson_id: int):
        await self.session.execute(
            Mark.__table__.delete().where(and_(Mark.student_id == student_id, Mark.lesson_id == lesson_id))
        )
        await self.commit()

    async def get_subjects_for_student(self, student_id: int) -> list[int]:
        results = await self.session.execute(
            select(Mark.subject_id).where(Mark.student_id == student_id).distinct()
        )

        return results.scalars().all()




