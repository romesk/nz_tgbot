
from sqlalchemy import Column, BigInteger, String, Date, DateTime, Integer, func

from src.database.models import Base


class Mark(Base):
    __tablename__ = "marks"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(BigInteger)
    student_id = Column(BigInteger)
    subject = Column(String(50))
    subject_id = Column(BigInteger)
    mark = Column(Integer)
    lesson_date = Column(Date())
    lesson_type = Column(String(50))
    comment = Column(String(1024))
    lesson_id = Column(BigInteger)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
