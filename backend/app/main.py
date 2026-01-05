from fastapi import FastAPI
from app.api import router
from app.core.config import settings
import fastapi_cdn_host


app = FastAPI(title=settings.PROJECT_NAME)
fastapi_cdn_host.patch_docs(app)


# 注册API路由
app.include_router(router.api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}
