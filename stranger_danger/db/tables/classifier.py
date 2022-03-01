from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import BLOB

from stranger_danger.db.config.settings import Base


class Classifier(Base):
    """ORM Model of Detector"""

    id = Column(Integer, nullable=False)
    model = Column(BLOB)
    date = Column(DateTime, func.now())
