from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.db.pgsql_session import Base
import enum
from sqlalchemy.orm import mapped_column,Mapped
from datetime import datetime
from app.schemas.user import GenderEnum
from pwdlib import PasswordHash
from app.utils.security import generate_uuid

#pip install "pwdlib[argon2]" 哈希加密密码

password_hash = PasswordHash.recommended()

class User(Base):
    __tablename__ = "users"  # 数据库中的表名
    
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    uuid: Mapped[int] = mapped_column(String(255),primary_key=True,default=generate_uuid())
    avatar_url: Mapped[str] = mapped_column(String(255),nullable=True)
    username: Mapped[str] = mapped_column(String(50),default='初遇')
    phone_nbr: Mapped[str] = mapped_column(String(50),unique=True,nullable=True)
    email: Mapped[str] = mapped_column(String(50), unique=True,nullable=True)
    _password: Mapped[str] = mapped_column(String(255),nullable=True)

    # 性别字段：使用之前定义的枚举
    gender: Mapped[str] = mapped_column(Enum(GenderEnum),default=GenderEnum.UNKNOWN)
    birthday: Mapped[str] = mapped_column(String(50),default="2000-01-01")
    Motto:Mapped[str] = mapped_column(String(255),default='当代码替你奔跑，心灵便有了仰望星空的闲暇')

    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # 时间戳：自动记录创建和更新时间
    # 创建时间（首次插入时自动设置）
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # 使用数据库服务器时间
        nullable=False
    )
    
    # 更新时间（插入和更新时自动刷新）
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # 初始值
        onupdate=func.now(),        # 更新时自动刷新
        nullable=False
    )
    
    def __init__(self, *args, **kwargs):
        password = kwargs.pop('password', None) # 1. 提取并移除password参数，如果没有则为None
        super().__init__(*args,**kwargs)  # 2. 调用父类初始化
        if password:                      # 3. 处理密码设置
            self.password = password
    
    @property # getter方法获取属性值时调用的方法
    def password(self):
        return self._password
    
    @password.setter # 设置属性值时调用的方法
    def password(self,raw_password):
        self._password = password_hash.hash(raw_password)
    
    def check_password(self,raw_password):
        return password_hash.verify(raw_password,self.password)
    

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
