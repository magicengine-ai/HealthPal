"""
健康指标模型
"""
from sqlalchemy import Column, BigInteger, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class HealthIndicator(Base):
    """健康指标表"""
    __tablename__ = "health_indicators"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键 ID")
    uuid = Column(String(36), unique=True, nullable=False, index=True, comment="指标 UUID")
    record_id = Column(BigInteger, ForeignKey("health_records.id"), nullable=False, index=True, comment="档案 ID")
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True, comment="用户 ID")
    member_id = Column(BigInteger, ForeignKey("family_members.id"), index=True, comment="家庭成员 ID")
    
    indicator_code = Column(String(50), nullable=False, index=True, comment="指标代码（如：WBC、RBC）")
    indicator_name = Column(String(100), nullable=False, comment="指标名称（如：白细胞、红细胞）")
    value = Column(String(50), nullable=False, comment="检测值")
    unit = Column(String(20), comment="单位")
    reference_min = Column(String(20), comment="参考范围最小值")
    reference_max = Column(String(20), comment="参考范围最大值")
    status = Column(String(20), comment="状态：normal/low/high/abnormal")
    
    test_date = Column(Date, nullable=False, index=True, comment="检测日期")
    
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    record = relationship("HealthRecord", back_populates="indicators")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
    
    def __repr__(self):
        return f"<HealthIndicator(uuid={self.uuid}, code={self.indicator_code}, value={self.value})>"
