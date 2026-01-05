import aioredis
from core import config


# 创建Redis连接
async def get_redis_connection():
    redis = await aioredis.from_url(config.REDIS_URL, encoding="utf-8",decode_responses=True)
    return redis

# 获取 Redis 连接
async def get_db():
    redis = await get_redis_connection()
    try:
        yield redis
    finally:
        await redis.close()

