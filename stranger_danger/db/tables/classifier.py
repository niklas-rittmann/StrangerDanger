from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import BLOB

Base = declarative_base()


class Classifier(Base):
    """ORM Model of Detector"""

    id = Column(Integer, nullable=False)
    model = Column(BLOB)
    date = Column(DateTime, func.now())
