from sqlalchemy import DateTime, Integer, func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from stranger_danger.db.config.settings import Base


class Email(Base):
    """ORM Model of Email"""

    __tablename__ = "email"
    id = Column(Integer, primary_key=True)
    address = Column(String(400))
    area = Column(Integer)
    date = Column(DateTime, server_default=func.now())
