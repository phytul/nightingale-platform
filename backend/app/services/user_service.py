from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_user
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import get_password_hash
from app.api.deps import DBDep


class UserService:
    def register_user(self, db: DBDep, user_in: UserCreate):
        # 逻辑检查
        existing_user = crud_user.get_by_email(db, user_in.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # 密码加密
        hashed_pwd = get_password_hash(user_in.password)

        # 调用 CRUD
        return crud_user.create(db, user_in, hashed_pwd)


# 定义 Service 的注入别名
UserServiceDep = Annotated[UserService, Depends(UserService)]


def update_user_profile(db: Session, user_id: int, update_data: UserUpdate):
    user = crud_user.get(db, user_id=user_id)
    if not user:
        raise Exception("User not found")
    return crud_user.update(db, db_obj=user, obj_in=update_data)
