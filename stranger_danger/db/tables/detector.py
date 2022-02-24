from sqlalchemy import JSON, Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import Column

Base = declarative_base()


class Detector(Base):
    """ORM Model of Detector"""

    id = Column(Integer, nullable=False)
    definition = Column(JSON)
    date = Column(DateTime, func.now())
