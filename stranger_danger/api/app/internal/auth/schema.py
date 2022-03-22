from pydantic.main import BaseModel


class AuthDetails(BaseModel):
    username: str
    password: str
