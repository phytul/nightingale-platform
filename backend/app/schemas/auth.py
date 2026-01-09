from enum import Enum
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
from .user import GenderEnum  # Import GenderEnum from user schema

UsernameStr = Annotated[str, Field(..., min_length=0, max_length=50, description="用户名")]
PasswordStr = Annotated[str, Field(..., min_length=6, max_length=20, description="密码")]
UuidInt = Annotated[int, Field(..., description="账户号")]
PhoneStr = Annotated[str, Field(...,min_length=11, max_length=11,pattern=r"^1[3-9]\d{9}$",  # 1开头，第二位3-9，共11位数字
        description="中国大陆手机号(11位数字,如13800138000)")]

def get_deadline():
    return datetime.now() + timedelta(minutes=20)

class UserSchema(BaseModel):
    id: int
    username: UsernameStr
    email: EmailStr
    sex: GenderEnum  # Add the sex field to match the endpoint

class LoginPasswordIn(BaseModel):
    email: EmailStr
    password: PasswordStr

class LoginAndRegisterCodeIn(BaseModel):
    email: EmailStr
    code: Annotated[str, Field(..., min_length=6, max_length=6, description="验证码")]
    dealine: datetime = Field(default_factory=get_deadline) # 自动计算

class LoginOut(BaseModel):
    user: UserSchema
    token: str



