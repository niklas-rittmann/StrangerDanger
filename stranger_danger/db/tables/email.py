from sqlalchemy import JSON, Column, DateTime, Integer, func
from sqlalchemy.sql.schema import Column

from stranger_danger.db.config.settings import Base


class Email(Base):
    """ORM Model of Email"""

    id = Column(Integer, nullable=False)
    definition = Column(JSON)
    date = Column(DateTime, func.now())
