"""
用药提醒模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, func, JSON, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class MedicationReminder(Base):
    """用药提醒表"""
    __tablename__ = "medication_reminders"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键 ID")
    uuid = Column(String(36), unique=True, nullable=False, index=True, comment="提醒 UUID")
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True, comment="用户 ID")
    member_id = Column(BigInteger, ForeignKey("family_members.id"), index=True, comment="家庭成员 ID")
    
    medication_name = Column(String(100), nullable=False, comment="药品名称")
    dosage = Column(String(50), comment="每次用量")
    frequency = Column(String(50), nullable=False, comment="用药频率：每日 n 次/每周 n 次）
    timing = Column(JSON, comment="用药时间：[{"time": "08:00", "meals": "before"}, ...]）
    
    start_date = Column(DateTime, nullable=False, comment="开始日期")
    end_date = Column(DateTime, comment="结束日期")
    
    is_active = Column(Boolean, default=True, index=True, comment="是否启用")
    is_completed = Column(Boolean, default=False, comment="是否已完成")
    
    instructions = Column(String(500), comment="用药说明")
    notes = Column(String(200), comment="备注")
    
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted_at = Column(DateTime, index=True, comment="删除时间（软删除）")
    
    # 关联关系
    user = relationship("User", back_populates="medication_reminders")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
    
    def __repr__(self):
        return f"<MedicationReminder(uuid={self.uuid}, name={self.medication_name})>"
