from pydantic import BaseModel


class AreaBase(BaseModel):
    id: int
    status: str
