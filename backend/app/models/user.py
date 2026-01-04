from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.db.session import Base
import enum

from app.schemas.user import GenderEnum


class User(Base):
    __tablename__ = "users"  # 数据库中的表名

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # 性别字段：使用之前定义的枚举
    gender = Column(Enum(GenderEnum), default=GenderEnum.UNKNOWN)

    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # 时间戳：自动记录创建和更新时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
