from datetime import timedelta

class Settings:
    PROJECT_NAME: str = "Nightingale Platform"

settings = Settings()

# 验证码获取配置
EXPIRE_TIMES = {
                "register": 600,      # 10分钟
                "login": 300,         # 5分钟  
                "reset_password": 900,# 15分钟
                "bind_email": 600     # 10分钟
            }

# 数据库连接配置
MYSQL_DB_URL = "mysql+aiomysql://root:123456@localhost:3306/zhiliao_ainame?charset=utf8"
PGSQL_DB_URL = "postgresql+asyncpg://root:123456@localhost:5432/nightingale"
REDIS_URL = "redis://localhost:6379"

# JWT配置
JWT_SECRET_KEY = "fgjktyu7564wef"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
JWT_REFRESH_TOKEN_EXPIRES =  timedelta(days=15)

# 邮箱相关配置
MAIL_USERNAME="1850453945@qq.com"
MAIL_PASSWORD="tqhsnsgxlbqlbfef"
MAIL_FROM="1850453945@qq.com"
MAIL_PORT=587
MAIL_SERVER="smtp.qq.com"
MAIL_FROM_NAME="夜莺出动"
MAIL_STARTTLS=True
MAIL_SSL_TLS=False