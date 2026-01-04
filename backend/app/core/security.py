from datetime import datetime, timedelta
# from jose import jwt
from app.core.config import settings

def create_access_token(subject: str | any) -> str:
    print('处理 JWT/OAuth2、令牌过期、Token 生成（依赖环境变量）。')