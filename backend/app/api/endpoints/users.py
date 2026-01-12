from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import GenderEnum,UserCreateSchema
from app.schemas.auth import LoginPasswordIn,LoginAndRegisterCodeIn,LoginOut
from app.db.pgsql_session import AsyncSession
from app.api.deps import get_pgsql_db, get_redis_db
from app.crud.crud_user import crud_user

router = APIRouter(prefix="/auth")


@router.post("/create_user")
async def create_user(
    user: UserCreateSchema,
    session: AsyncSession = Depends(get_pgsql_db)
):
    await crud_user.create_user(session,obj_in=user)
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
    用
    """
    pass

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