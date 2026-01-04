from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Annotated
from fastapi import Depends

# 1. 数据库连接配置 (实际开发建议放 app/core/config.py)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/dbname"
# 如果是 SQLite，写法如下：
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. 创建数据库引擎 (Engine)
# check_same_thread=False 仅在 SQLite 下需要
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 每次使用连接前检测是否存活，防止“连接断开”错误
    echo=False,  # 设置为 True 可以打印所有 SQL 语句，方便调试
)

# 3. 定义 SessionLocal 类
# 注意：这只是个类，还没产生真正的实例
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 定义 Base 类，供 models/ 中的模型继承
Base = declarative_base()
