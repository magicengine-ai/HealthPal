"""
通用 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List
from datetime import datetime

T = TypeVar('T')


class ResponseModel(BaseModel):
    """通用响应模型"""
    code: int = Field(0, description="错误码：0 表示成功")
    message: str = Field("success", description="响应消息")
    data: Optional[dict] = Field(None, description="响应数据")


class PageResponse(BaseModel):
    """分页响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")
    items: List[dict] = Field(..., description="数据列表")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    code: int = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    details: Optional[dict] = Field(None, description="详细错误信息")


class TokenData(BaseModel):
    """Token 数据 Schema"""
    uuid: Optional[str] = None


class CurrentUser(BaseModel):
    """当前用户信息"""
    uuid: str
    user_id: int
    phone: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
