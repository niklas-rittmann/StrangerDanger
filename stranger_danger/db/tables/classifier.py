from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import LargeBinary

from stranger_danger.db.config.settings import Base


class Classifier(Base):
    """ORM Model of Detector"""

    __tablename__ = "classifier"
    id = Column(Integer, primary_key=True)
    model = Column(LargeBinary)
    date = Column(DateTime, server_default=func.now())
