from enum import Enum
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field

UsernameStr = Annotated[
    str, Field(..., min_length=3, max_length=20, description="用户名")
]

PassordStr = Annotated[str, Field(..., min_length=6, max_length=20, description="密码")]


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


Gender = Annotated[
    GenderEnum,
    Field(
        default=GenderEnum.UNKNOWN,
        description="用户性别: male(男), female(女), other(其他), unknown(未知)",
    ),
]


class UserSchema(BaseModel):
    id: Annotated[int, Field(...)]
    username: UsernameStr
    password: PassordStr
    sex: Gender
    email: EmailStr


class UserCreate(BaseModel):
    username: UsernameStr
    password: PassordStr
    sex: Gender
    email: EmailStr


class UserUpdate(BaseModel):
    username: UsernameStr
    password: PassordStr
    sex: Gender
    email: EmailStr
    is_active: bool = True


class UserOut(BaseModel):
    id: int
    username: UsernameStr
    password: PassordStr
    sex: Gender
    email: EmailStr
    is_active: bool = True
