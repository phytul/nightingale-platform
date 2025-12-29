from fastapi import FastAPI
from app.api import router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# 注册API路由
app.include_router(router.api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}
