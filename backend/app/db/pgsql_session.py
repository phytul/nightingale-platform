# - * - encoding:utf-8 - * -
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from app.core import config

# 创建异步引擎
pgsql_engine = create_async_engine(
    config.PGSQL_DB_URL,
    echo=True, # 可选，输出SQL日志
    pool_pre_ping=True,  # 每次使用连接前检测是否存活，防止“连接断开”错误
    pool_size=10, # 设置连接池中保持的持久连接数
    max_overflow=20 # 设置连接池中允许创建的额外连接数
)

# 创建会话工厂
PgsqlAsyncSessionFactory = sessionmaker(
    # Engine或者其子类对象（这里是AsyncEngine）
    bind=pgsql_engine,
    # Session类的代替（默认是Session类）
    class_=AsyncSession,
    # 是否在查找之前执行flush操作（默认是True）
    autoflush=True,
    # 是否在执行commit操作后Session就过期（默认是True）
    expire_on_commit=False
)

SessionLocal = sessionmaker(bind=pgsql_engine)

# 定义命名约定的Base类
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        # ix: index，索引。
        "ix": 'ix_%(column_0_label)s',
        # un：unique，唯一约束
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        # ck：Check，检查约束
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        # fk：Foreign Key，外键约束
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        # pk：Primary Key，主键约束
        "pk": "pk_%(table_name)s"
    })