from typing import Annotated
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.pgsql_session import SessionLocal, PgsqlAsyncSessionFactory
from app.db.redis_session import get_redis_connection
from fastapi_mail import FastMail
from app.utils.email_util import create_qqmail_instance
from redis.asyncio import Redis

# 获取 mail 连接
async def get_mail()-> FastMail:
    return create_qqmail_instance()

# 获取 pgsql 连接
async def get_pgsql_db():
    try:
        db =  PgsqlAsyncSessionFactory()
        yield db
    finally:
        await db.close()

# 获取 Redis 连接
async def get_redis_db():
    redis_db = await get_redis_connection()  # 使用 await 调用异步函数

    if redis_db is None:
        # 根据业务需求决定是抛出异常还是返回 None
        raise HTTPException(status_code=503, detail="Redis service unavailable")
    
    try:
        yield redis_db
    finally:
        # 安全关闭连接：检查 redis_db 不是 None 且有 close 方法
        if redis_db is not None and hasattr(redis_db, 'close'):
            try:
                await redis_db.close()
            except Exception as e:
                # 记录错误但不中断程序
                print(f"Warning: Failed to close Redis connection: {e}")

# 定义重用的类型别名
PGSQL_DBDep = Annotated[Session, Depends(get_pgsql_db)]
REDIS_DBDep = Annotated[Redis, Depends(get_redis_db)]
