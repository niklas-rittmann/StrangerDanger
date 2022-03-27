from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class EmailSchema(BaseModel):
    address: EmailStr
    area: int


class EmailId(EmailSchema):
    id: int


class EmailStatus(EmailSchema):
    status: str
