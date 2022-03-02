from sqlalchemy import JSON, Column, DateTime, Integer, func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import BLOB, Float

from stranger_danger.db.config.settings import Base


class Predictions(Base):
    """ORM Model of Predictions"""

    id = Column(Integer, nullable=False)
    image = Column(BLOB, nullable=False)
    confidence = Column(Float, nullable=False)
    date = Column(DateTime, func.now())
