from pydantic import BaseModel


class User(BaseModel):
    id: int
    sex: str
    username: str
    email: str
