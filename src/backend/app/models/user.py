"""
用户模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Date, SmallInteger, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键 ID")
    uuid = Column(String(36), unique=True, nullable=False, index=True, comment="用户 UUID")
    phone = Column(String(20), unique=True, index=True, comment="手机号")
    email = Column(String(100), index=True, comment="邮箱")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    nickname = Column(String(50), comment="昵称")
    avatar_url = Column(String(255), comment="头像 URL")
    gender = Column(String(1), default="0", comment="性别 0:未知 1:男 2:女")
    birthday = Column(Date, comment="生日")
    
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted_at = Column(DateTime, nullable=True, index=True, comment="删除时间")
    
    # 关联关系
    family_members = relationship("FamilyMember", back_populates="user", cascade="all, delete-orphan")
    health_records = relationship("HealthRecord", back_populates="user", cascade="all, delete-orphan")
    medication_reminders = relationship("MedicationReminder", back_populates="user", cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
    
    def __repr__(self):
        return f"<User(id={self.id}, phone={self.phone}, nickname={self.nickname})>"
