"""
家庭成员模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class FamilyMember(Base):
    """家庭成员表"""
    __tablename__ = "family_members"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键 ID")
    uuid = Column(String(36), unique=True, nullable=False, index=True, comment="成员 UUID")
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True, comment="用户 ID")
    
    name = Column(String(50), nullable=False, comment="姓名")
    relation = Column(String(20), nullable=False, comment="关系：父子/母子/夫妻等")
    gender = Column(String(1), default="0", comment="性别 0:未知 1:男 2:女")
    birthday = Column(DateTime, comment="生日")
    phone = Column(String(20), comment="手机号")
    remark = Column(String(200), comment="备注")
    
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted_at = Column(DateTime, index=True, comment="删除时间（软删除）")
    
    # 关联关系
    user = relationship("User", back_populates="family_members")
    health_records = relationship("HealthRecord", back_populates="member", cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
    
    def __repr__(self):
        return f"<FamilyMember(uuid={self.uuid}, name={self.name})>"
