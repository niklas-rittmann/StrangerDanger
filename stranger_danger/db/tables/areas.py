from sqlalchemy import DateTime, Integer, func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from stranger_danger.db.config.settings import Base


class Areas(Base):
    """ORM Model of Fences"""

    __tablename__ = "areas"
    id = Column(Integer, primary_key=True)
    directory = Column(String(400))
    date = Column(DateTime, server_default=func.now())
