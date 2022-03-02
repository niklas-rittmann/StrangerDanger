from sqlalchemy import JSON, Column, DateTime, Integer, func
from sqlalchemy.sql.schema import Column

from stranger_danger.db.config.settings import Base


class Email(Base):
    """ORM Model of Email"""

    __tablename__ = "email"
    id = Column(Integer, primary_key=True)
    definition = Column(JSON)
    date = Column(DateTime, server_default=func.now())
