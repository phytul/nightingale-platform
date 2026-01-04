from enum import Enum
from pydantic import BaseModel


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


class User(BaseModel):
    id: int
    sex: Gender
    username: str
    email: str
