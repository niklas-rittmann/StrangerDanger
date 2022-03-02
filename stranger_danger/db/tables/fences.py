from sqlalchemy import JSON, Column, DateTime, Integer, func
from sqlalchemy.sql.schema import Column

from stranger_danger.db.config.settings import Base


class Fences(Base):
    """ORM Model of Fences"""

    __tablename__ = "fences"
    id = Column(Integer, primary_key=True)
    definition = Column(JSON)
    date = Column(DateTime, server_default=func.now())
