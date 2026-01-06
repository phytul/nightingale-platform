from fastapi import HTTPException
from fastapi import FastAPI, Depends
from redis.asyncio import Redis
from db.redis_session import get_db

# 创建/设置数据
async def set_key(key: str, 
                value: str, 
                expir: int = 0, 
                redis: Redis = Depends(get_db)):
    try:
        if expir > 0:
            await redis.set(key, value, ex=expir)
        else:
            await redis.set(key, value)  # 设置键值对
        return {"message": "Key set successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取数据
async def get_key(key: str, 
                  redis: Redis = Depends(get_db)):
    value = await redis.get(key)  # 获取键对应的值
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}


# 更新数据
async def update_key(
        key: str, 
        value: str, 
        expir: int = 0,
        redis: Redis = Depends(get_db)):
    exists = await redis.exists(key)
    if not exists:
        raise HTTPException(status_code=404, detail="Key not found")
    if expir > 0:
        await redis.set(key, value, ex=expir)
    else:
        await redis.set(key, value)  # 更新键值对
    return {"message": "Key updated successfully"}

# 删除数据
async def delete_key(
        key: str, 
        redis: Redis = Depends(get_db)):
    result = await redis.delete(key)  # 删除指定键
    if result == 0:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"message": "Key deleted successfully"}

"""
redis.set(key, value, ex=expiration)  # 设置过期时间
还有管道功能和事务管理
"""

