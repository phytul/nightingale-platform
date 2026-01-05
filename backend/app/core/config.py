from datetime import timedelta

class Settings:
    PROJECT_NAME: str = "Nightingale Platform"


settings = Settings()

MYSQL_DB_URL = "mysql+aiomysql://root:123456@localhost:3306/zhiliao_ainame?charset=utf8"

JWT_SECRET_KEY = "fgjktyu7564wef"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
JWT_REFRESH_TOKEN_EXPIRES =  timedelta(days=15)