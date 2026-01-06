from enum import Enum
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field

UsernameStr = Annotated[str, Field(..., min_length=0, max_length=50, description="用户名")]
PassordStr = Annotated[str, Field(..., min_length=6, max_length=20, description="密码")]
UuidInt = Annotated[int, Field(..., description="账户号")]
PhoneStr = Annotated[str, Field(...,min_length=11, max_length=11,pattern=r"^1[3-9]\d{9}$",  # 1开头，第二位3-9，共11位数字
        description="中国大陆手机号(11位数字,如13800138000)")]

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

Gender = Annotated[GenderEnum,Field(default=GenderEnum.UNKNOWN,description="用户性别: male(男), female(女), other(其他), unknown(未知)",),]

class UserCreateSchema(BaseModel):
    uuid: UuidInt
    username: UsernameStr
    phone_nbr: PhoneStr
    

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
