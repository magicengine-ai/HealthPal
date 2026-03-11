"""
用药提醒 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MedicationTiming(BaseModel):
    """用药时间"""
    time: str = Field(..., pattern=r"^[0-2][0-9]:[0-5][0-9]$", description="时间 HH:MM")
    meals: str = Field("after", description="餐前餐后：before/after/empty")


class MedicationBase(BaseModel):
    """用药提醒基础 Schema"""
    medication_name: str = Field(..., min_length=1, max_length=100, description="药品名称")
    dosage: Optional[str] = Field(None, max_length=50, description="每次用量")
    frequency: str = Field(..., min_length=1, max_length=50, description="用药频率")
    timing: Optional[List[MedicationTiming]] = Field(None, description="用药时间")
    start_date: datetime = Field(..., description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    instructions: Optional[str] = Field(None, max_length=500, description="用药说明")
    notes: Optional[str] = Field(None, max_length=200, description="备注")


class MedicationCreate(MedicationBase):
    """用药提醒创建 Schema"""
    member_id: Optional[int] = Field(None, description="家庭成员 ID")


class MedicationUpdate(BaseModel):
    """用药提醒更新 Schema"""
    medication_name: Optional[str] = Field(None, min_length=1, max_length=100, description="药品名称")
    dosage: Optional[str] = Field(None, max_length=50, description="每次用量")
    frequency: Optional[str] = Field(None, min_length=1, max_length=50, description="用药频率")
    timing: Optional[List[MedicationTiming]] = Field(None, description="用药时间")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    instructions: Optional[str] = Field(None, max_length=500, description="用药说明")
    notes: Optional[str] = Field(None, max_length=200, description="备注")
    is_active: Optional[bool] = Field(None, description="是否启用")


class MedicationResponse(MedicationBase):
    """用药提醒响应 Schema"""
    uuid: str
    user_id: int
    member_id: Optional[int] = None
    id: Optional[int] = None
    is_active: bool = True
    is_completed: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MedicationListResponse(BaseModel):
    """用药提醒列表响应"""
    total: int
    page: int
    page_size: int
    medications: List[MedicationResponse]


class MedicationConfirmRequest(BaseModel):
    """用药确认请求"""
    taken_time: Optional[datetime] = Field(None, description="实际服药时间")
    notes: Optional[str] = Field(None, max_length=200, description="备注")
