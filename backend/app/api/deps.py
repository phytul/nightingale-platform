from typing import Annotated, Generator
from fastapi import Depends, status
from sqlalchemy.orm import Session
from app.db.pgsql_session import SessionLocal, PgsqlAsyncSessionFactory
from app.db.redis_session import get_redis_connection

# 获取 pgsql 连接
async def get_pgsql_db():
    try:
        db =  PgsqlAsyncSessionFactory()
        yield db
    finally:
        await db.close()

# 获取 Redis 连接
async def get_redis_db():
    redis = get_redis_connection()
    try:
        yield redis
    finally:
        await redis.close()


# 定义重用的类型别名
PGSQL_DBDep = Annotated[Session, Depends(get_pgsql_db)]
REDIS_DBDep = Annotated[Session, Depends(get_redis_db)]
