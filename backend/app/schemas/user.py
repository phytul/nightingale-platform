from enum import Enum
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

UsernameStr = Annotated[str, Field(..., min_length=0, max_length=50, description="用户名")]
PasswordStr = Annotated[str, Field(..., min_length=6, max_length=20, description="密码")]
UuidInt = Annotated[int, Field(..., description="账户号")]
PhoneStr = Annotated[str, Field(...,min_length=11, max_length=11,pattern=r"^1[3-9]\d{9}$",  # 1开头，第二位3-9，共11位数字
        description="中国大陆手机号(11位数字,如13800138000)")]

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

GenderStr = Annotated[GenderEnum,Field(default=GenderEnum.UNKNOWN,description="用户性别: male(男), female(女), other(其他), unknown(未知)",),]

class UserCreateSchema(BaseModel):
    uuid: UuidInt
    username: UsernameStr
    phone_nbr: PhoneStr
    email: EmailStr
    password: PasswordStr
    gender: GenderStr
    birthday: Annotated[str, Field(
        default="2000-01-01",  # 默认值
        min_length=10,          # yyyy-mm-dd 固定10字符
        max_length=10,          # 严格限制长度
        pattern=r"^\d{4}-\d{2}-\d{2}$",  # 正则验证格式
        description="生日 (格式: yyyy-mm-dd)"
    )]
    Motto: Annotated[str, Field(
        default='当代码替你奔跑，心灵便有了仰望星空的闲暇',
        description="个性签名"
    )]

    # 额外验证日期有效性（可选）
    @field_validator('birthday')
    def validate_birthday_format(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            raise ValueError("生日格式无效，请使用 yyyy-mm-dd 格式")

