from fastapi import FastAPI
from app.api import router
from app.core.config import settings
import fastapi_cdn_host
from db.redis_session import get_redis_connection


app = FastAPI(title=settings.PROJECT_NAME)
fastapi_cdn_host.patch_docs(app)

# 在应用启动时初始化 Redis 连接
@app.on_event("startup")
async def on_startup():
    redis = await get_redis_connection()
    print("Redis connection initialized")
    await redis.close()

# 注册API路由
app.include_router(router.api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}
