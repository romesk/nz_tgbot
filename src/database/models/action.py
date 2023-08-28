from sqlalchemy import Column, BigInteger, String, DateTime, func

from src.database.models import Base


class Action(Base):
    __tablename__ = "actions"

    action_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(BigInteger)
    student_id = Column(BigInteger)
    action = Column(String(256))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
