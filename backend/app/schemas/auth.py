from enum import Enum
from typing import Annotated, Union
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
from .user import GenderEnum  # Import GenderEnum from user schema

UsernameStr = Annotated[str, Field(..., min_length=0, max_length=50, description="用户名")]
PasswordStr = Annotated[str, Field(..., min_length=6, max_length=20, description="密码")]
UuidInt = Annotated[int, Field(..., description="账户号")]
PhoneStr = Annotated[Union[str,None], Field(None,min_length=11, max_length=11,pattern=r"^1[3-9]\d{9}$",  # 1开头，第二位3-9，共11位数字
        description="中国大陆手机号(11位数字,如13800138000)")]
AvatarStr = Annotated[Union[str,None], Field(None, description="头像图片地址")]
CodeStr = Annotated[str, Field(..., min_length=6, max_length=6, description="验证码")]

class ExpireEnum(str, Enum):
    REGISTER = "register"
    LOGIN = "login"
    RESET_PASSWORD = "reset_password"
    BIND = "bind_email"

class LoginAndRegisterCodeIn(BaseModel):
    email: EmailStr
    code: CodeStr
    type: ExpireEnum

class UserSchema(BaseModel):
    id: int
    username: UsernameStr
    avatar_url: AvatarStr

class LoginPasswordIn(BaseModel):
    email: EmailStr
    password: PasswordStr

class LoginOut(BaseModel):
    token: str
    user: UserSchema
    



