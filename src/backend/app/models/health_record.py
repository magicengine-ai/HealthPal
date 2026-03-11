"""
健康档案模型
"""
from sqlalchemy import Column, BigInteger, String, Date, DateTime, ForeignKey, func, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class HealthRecord(Base):
    """健康档案表"""
    __tablename__ = "health_records"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键 ID")
    uuid = Column(String(36), unique=True, nullable=False, index=True, comment="档案 UUID")
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True, comment="用户 ID")
    member_id = Column(BigInteger, ForeignKey("family_members.id"), index=True, comment="家庭成员 ID")
    
    record_type = Column(String(50), nullable=False, index=True, comment="档案类型")
    title = Column(String(200), nullable=False, comment="档案标题")
    hospital = Column(String(100), comment="医院名称")
    department = Column(String(50), comment="科室")
    record_date = Column(Date, nullable=False, index=True, comment="检查日期")
    
    ocr_status = Column(String(20), default="pending", comment="OCR 状态：pending/processing/completed/failed")
    ocr_result = Column(JSON, comment="OCR 识别结果（原始 JSON）")
    structured_data = Column(JSON, comment="结构化数据（提取的指标等）")
    tags = Column(JSON, comment="标签数组")
    file_urls = Column(JSON, comment="文件 URL 列表")
    
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted_at = Column(DateTime, index=True, comment="删除时间（软删除）")
    
    # 关联关系
    user = relationship("User", back_populates="health_records")
    member = relationship("FamilyMember", back_populates="health_records")
    indicators = relationship("HealthIndicator", back_populates="record", cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
    
    def __repr__(self):
        return f"<HealthRecord(uuid={self.uuid}, title={self.title})>"
