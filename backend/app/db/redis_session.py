from redis.asyncio import Redis
from app.core import config


# 创建Redis连接
async def get_redis_connection():
    redis = await Redis.from_url(config.REDIS_URL, encoding="utf-8",decode_responses=True)
    return redis


