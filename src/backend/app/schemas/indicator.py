"""
健康指标 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


class IndicatorBase(BaseModel):
    """健康指标基础 Schema"""
    indicator_code: str = Field(..., min_length=1, max_length=50, description="指标代码")
    indicator_name: str = Field(..., min_length=1, max_length=100, description="指标名称")
    value: str = Field(..., min_length=1, max_length=50, description="检测值")
    unit: Optional[str] = Field(None, max_length=20, description="单位")
    reference_min: Optional[str] = Field(None, max_length=20, description="参考范围最小值")
    reference_max: Optional[str] = Field(None, max_length=20, description="参考范围最大值")
    status: Optional[str] = Field(None, description="状态：normal/low/high/abnormal")
    test_date: date = Field(..., description="检测日期")


class IndicatorCreate(IndicatorBase):
    """健康指标创建 Schema"""
    record_uuid: str = Field(..., description="所属档案 UUID")
    member_id: Optional[int] = Field(None, description="家庭成员 ID")


class IndicatorUpdate(BaseModel):
    """健康指标更新 Schema"""
    value: Optional[str] = Field(None, min_length=1, max_length=50, description="检测值")
    unit: Optional[str] = Field(None, max_length=20, description="单位")
    reference_min: Optional[str] = Field(None, max_length=20, description="参考范围最小值")
    reference_max: Optional[str] = Field(None, max_length=20, description="参考范围最大值")
    status: Optional[str] = Field(None, description="状态")


class IndicatorResponse(IndicatorBase):
    """健康指标响应 Schema"""
    uuid: str
    record_id: int
    user_id: int
    member_id: Optional[int] = None
    id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class IndicatorTrendData(BaseModel):
    """指标趋势数据"""
    indicator_code: str
    indicator_name: str
    unit: Optional[str] = None
    reference_min: Optional[str] = None
    reference_max: Optional[str] = None
    data_points: List[dict]  # [{date: "2024-01-01", value: "5.2"}, ...]


class IndicatorTrendResponse(BaseModel):
    """指标趋势响应"""
    indicators: List[IndicatorTrendData]
    total: int


class IndicatorListResponse(BaseModel):
    """健康指标列表响应"""
    total: int
    page: int
    page_size: int
    indicators: List[IndicatorResponse]
