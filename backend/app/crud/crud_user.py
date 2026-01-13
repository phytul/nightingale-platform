from typing import Optional, List
from sqlalchemy.orm import Session
from app.schemas.user import UserCreateSchema, UserUpdateSchema
from app.db.pgsql_session import AsyncSession
from app.models.user import User
from sqlalchemy import select, update, delete, exists
from datetime import datetime, timedelta

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session= session
    
    async def get_by_email(self, email: str) -> User | None:
        """根据邮箱获取用户"""
        async with self.session.begin():
            user = await self.session.scalar(select(User).where(User.email==email))
            return user
    
    async def email_is_exist(self, email: str) -> bool:
        """判断库中是否存在该邮箱"""
        async with self.session.begin():
            stmt = select(exists().where(User.email==email))
            return await self.session.scalar(stmt)
    
    async def create(self, user_schema: UserCreateSchema) -> User:
        """创建用户"""
        async with self.session.begin():
            user = User(**user_schema.model_dump()) # 转换成关键字字典的格式
            self.session.add(user)
            return user

    async def update(self, email: str, user_schema: UserUpdateSchema) -> User | None:
        """更新用户信息"""
        async with self.session.begin():
            stmt = (
                update(User)
                .where(User.email == email)
                .values(**user_schema.model_dump(exclude_unset=True))
                .returning(User)
            )
            result = await self.session.execute(stmt)
            updated_user = result.scalar_one_or_none()
            return updated_user

    async def delete(self, email: str) -> bool:
        """删除用户"""
        async with self.session.begin():
            stmt = delete(User).where(User.email == email)
            result = await self.session.execute(stmt)
            return result.rowcount > 0
        