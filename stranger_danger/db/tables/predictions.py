from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import BLOB, Float

from stranger_danger.db.config.settings import Base


class Predictions(Base):
    """ORM Model of Predictions"""

    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    image = Column(BLOB, nullable=False)
    confidence = Column(Float, nullable=False)
    date = Column(DateTime, server_default=func.now())
