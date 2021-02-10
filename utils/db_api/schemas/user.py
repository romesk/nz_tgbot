from sqlalchemy import Column, BigInteger, String, Integer, sql

from utils.db_api.postgresql import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True, unique=True)
    login = Column(String(40))
    password = Column(String(40))
    news = Column(Integer)

    query: sql.Select
