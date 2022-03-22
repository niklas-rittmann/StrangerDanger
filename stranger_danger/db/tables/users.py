from sqlalchemy import DateTime, Integer, func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from stranger_danger.db.config.settings import Base


class Users(Base):
    """ORM Model of Users"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    date = Column(DateTime, server_default=func.now())
