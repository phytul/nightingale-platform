from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import GenderEnum,UserCreateSchema
from app.schemas.auth import UserSchema
from app.db.pgsql_session import AsyncSession
from app.api.deps import get_pgsql_db, get_redis_db

router = APIRouter(prefix="/auth")


@router.post("/create_user")
async def create_user(
    user: UserCreateSchema,
    session: AsyncSession = Depends(get_pgsql_db)
):
    session.add(user)
    # 这段有问题，UserCreateSchema是pydantic的方法不是sqlachmey的模型，需要在crud里里写导入数据库的方法再调用
    return {
        "user": user
    }
