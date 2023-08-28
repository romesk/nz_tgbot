from sqlalchemy import Column, BigInteger, String, DateTime, func

from src.database.models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    fullname = Column(String(50))
    username = Column(String(50))
    fullname_nzua = Column(String(50))
    student_id = Column(BigInteger)
    login = Column(String(50))
    password = Column(String(50))
    access_token = Column(String(50))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
