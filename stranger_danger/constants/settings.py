from pydantic import BaseSettings
from pydantic.networks import EmailStr


class EmailSettings(BaseSettings):
    SENDER: str
    EMAIL_PASSWORD: str
    EMAIL_SERVER: str
    EMAIL_PORT: int
    EMAIL_SUBJECT: str
    EMAIL_RECEIVER: EmailStr


class DBSettings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_DATABASE: str


class AuthSettings(BaseSettings):
    SECRET: str
