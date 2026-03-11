"""
健康档案 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


class RecordBase(BaseModel):
    """健康档案基础 Schema"""
    record_type: str = Field(..., min_length=1, max_length=50, description="档案类型")
    title: str = Field(..., min_length=1, max_length=200, description="档案标题")
    hospital: Optional[str] = Field(None, max_length=100, description="医院名称")
    department: Optional[str] = Field(None, max_length=50, description="科室")
    record_date: date = Field(..., description="检查日期")


class RecordCreate(RecordBase):
    """健康档案创建 Schema"""
    member_id: Optional[int] = Field(None, description="家庭成员 ID")
    tags: Optional[List[str]] = Field(None, description="标签数组")


class RecordUpdate(BaseModel):
    """健康档案更新 Schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="档案标题")
    hospital: Optional[str] = Field(None, max_length=100, description="医院名称")
    department: Optional[str] = Field(None, max_length=50, description="科室")
    record_date: Optional[date] = Field(None, description="检查日期")
    tags: Optional[List[str]] = Field(None, description="标签数组")


class RecordResponse(RecordBase):
    """健康档案响应 Schema"""
    uuid: str
    user_id: int
    member_id: Optional[int] = None
    id: Optional[int] = None
    ocr_status: str = "pending"
    ocr_result: Optional[dict] = None
    structured_data: Optional[dict] = None
    tags: Optional[List[str]] = None
    file_urls: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RecordDetailResponse(RecordResponse):
    """健康档案详情响应（包含指标）"""
    indicators: Optional[List[dict]] = None


class RecordListResponse(BaseModel):
    """健康档案列表响应"""
    total: int
    page: int
    page_size: int
    records: List[RecordResponse]


class RecordUploadResponse(BaseModel):
    """档案上传响应"""
    record_id: str
    ocr_status: str
    message: str = "上传成功"
