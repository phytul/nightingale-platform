from app.schemas.auth import ExpireEnum
from app.core import config
from typing import Annotated
from redis.asyncio import Redis
from pydantic import Field
from pydantic import EmailStr
import string
import random
from fastapi_mail import FastMail, MessageSchema, MessageType
from aiosmtplib import SMTPResponseException
from app.crud.redis import CaptchaStorage
from fastapi import HTTPException, Query
from app.schemas import ResponseOut

async def send_captche(email :Annotated[EmailStr,Query(...)],
                       type :Annotated[ExpireEnum,Field(default=ExpireEnum.REGISTER,description="redis存储验证码的时间")],
                       mail :FastMail,
                       session :Redis
                       ):
    # 1.生成6位数验证码
    digits = string.digits
    code = ''.join(random.choices(digits, k=6))
    expire_time = int(config.EXPIRE_TIMES[type])/60
    # 2.创建消息对象
    message = MessageSchema(
        subject='【nightingale-夜莺】注册验证码',
        recipients=[email],
        body=f"您的验证码为：{code},{expire_time}分钟有效!请尽快验证",
        subtype=MessageType.plain # 纯文本
    )
    # 3.发送验证码
    try:
        await mail.send_message(message)
    except SMTPResponseException as e:
        if e.code == -1 and b"\\x00\\x00\\x00" in str(e).encode():
            print("忽略qq邮箱smtp关闭阶段的非标准响应(邮件已经发送成功)")
            # 4.将邮箱和验证码存储到数据库中
            redis_session = CaptchaStorage(session=session)
            await redis_session.store_email_code(email=email,code=code,scene=type)
        else:
            raise HTTPException(500,detail="邮件发送失败")
    return ResponseOut()