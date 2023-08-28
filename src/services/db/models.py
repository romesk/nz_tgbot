from sqlalchemy import Column, BigInteger, String, DateTime, func, Integer
from src.services.db.base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    fullname = Column(String(50))
    username = Column(String(50))
    login = Column(String(50))
    password = Column(String(50))
    access_token = Column(String(50))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Marks(Base):
    __tablename__ = "marks"

    mark_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(BigInteger)
    subject = Column(String(50))
    subject_id = Column(BigInteger)
    mark = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Actions(Base):
    __tablename__ = "actions"

    action_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(BigInteger)
    action = Column(String(256))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

