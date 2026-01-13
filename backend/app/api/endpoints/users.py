from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.user import GenderEnum,UserCreateSchema
from app.schemas.auth import LoginPasswordIn,LoginOut, ExpireEnum, LoginAndRegisterCodeIn
from app.db.pgsql_session import AsyncSession
from app.api.deps import get_pgsql_db, get_redis_db, get_mail
from app.crud.crud_user import UserRepository
from app.services.auth import AuthHandler
from typing import Annotated
from pydantic import EmailStr, Field
from redis.asyncio import Redis
from fastapi_mail import FastMail
from app.services.send_captche import send_captche

auth_handler = AuthHandler()
router = APIRouter(prefix="/auth")

@router.post("/send_code")
async def login_password(
    email: Annotated[EmailStr,Query(...)],
    type : Annotated[ExpireEnum,Field(default=ExpireEnum.REGISTER,description="redis存储验证码的时间")],             
    mail: FastMail = Depends(get_mail),
    session: Redis = Depends(get_redis_db)
)->LoginOut:
    responseout = send_captche(email,type,mail,session)
    return responseout

@router.post("/create_user")
async def create_user(
    user: UserCreateSchema,
    session: AsyncSession = Depends(get_pgsql_db)
):
    user_repo = UserRepository(session=session)
    await user_repo.create(session,obj_in=user)
    # 这段有问题，UserCreateSchema是pydantic的方法不是sqlachmey的模型，需要在crud里里写导入数据库的方法再调用
    return {
        "user": user
    }

@router.post("/login_password")
async def login_password(
    login_password: LoginPasswordIn,
    session: AsyncSession = Depends(get_pgsql_db)
)->LoginOut:
    """
    用密码登陆的接口r n
    params:
        LoginPasswordIn(email,password)
    return:
        LoginOut(token&user[id,username,email,sex])
    1、验证密码的准确性/用户名是否存在
    2、返回token和user
    """
    # 1.创建user_repo对象
    user_repo = UserRepository(session=session)
    # 2.根据邮箱查找用户
    user: UserCreateSchema|None = await user_repo.get_by_email(str(login_password.email))
    print(user)
    if not user:
        raise HTTPException(400,detail="该用户不存在!")
    if not user.check_password(login_password.password):
        raise HTTPException(400,detail="邮箱或密码错误!")
    # 3.生成JWToken
    tokens = auth_handler.encode_login_token(user.id)
    return {
        "token":tokens['access_token'],
        "user":user
    }

@router.post("/login_code")
async def login_password(
    login_password: LoginAndRegisterCodeIn,
    session: AsyncSession = Depends(get_pgsql_db)
)->LoginOut:
    pass

@router.post("/register_code")
async def login_password(
    login_password: LoginAndRegisterCodeIn,
    session: AsyncSession = Depends(get_pgsql_db)
)->LoginOut:
    pass