from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import get_password_hash


class CRUDUser:
    """
    用户模块的增删改查逻辑
    """

    def get(self, db: Session, user_id: int) -> Optional[User]:
        """根据 ID 获取单个用户"""
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """根据邮箱获取用户（常用于登录或唯一性检查）"""
        return db.query(User).filter(User.email == email).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        """批量获取用户列表（支持分页）"""
        return db.query(User).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """创建用户"""
        # 1. 准备数据（将 Schema 转为字典，并处理密码哈希）
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),  # 确保存储哈希值
            gender=obj_in.gender,
        )
        # 2. 写入数据库
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)  # 刷新以获取 ID 等自动生成的字段
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """更新用户信息"""
        # 将输入数据转为字典，排除未设置的字段
        update_data = obj_in.model_dump(exclude_unset=True)

        # 特殊处理密码：如果有新密码，需要哈希后再存
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            db_obj.hashed_password = hashed_password
            del update_data["password"]

        # 更新其他字段
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[User]:
        """删除用户"""
        obj = db.query(User).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# 实例化，方便在其他地方直接导入使用
crud_user = CRUDUser()
