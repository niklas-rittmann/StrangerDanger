from sqlalchemy.orm.decl_api import declarative_base

from stranger_danger.constants.settings import DBSettings

Db = DBSettings()

DB_USER = Db.DB_USER
DB_PASSWORD = Db.DB_PASSWORD
DB_HOST = Db.DB_HOST
DB_DATABASE = Db.DB_DATABASE
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

Base = declarative_base()
