"""
家庭成员 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FamilyMemberBase(BaseModel):
    """家庭成员基础 Schema"""
    name: str = Field(..., min_length=1, max_length=50, description="姓名")
    relation: str = Field(..., min_length=1, max_length=20, description="关系")
    gender: str = Field("0", pattern="^[012]$", description="性别 0:未知 1:男 2:女")
    birthday: Optional[datetime] = Field(None, description="生日")
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="手机号")
    remark: Optional[str] = Field(None, max_length=200, description="备注")


class FamilyMemberCreate(FamilyMemberBase):
    """家庭成员创建 Schema"""
    pass


class FamilyMemberUpdate(BaseModel):
    """家庭成员更新 Schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="姓名")
    relation: Optional[str] = Field(None, min_length=1, max_length=20, description="关系")
    gender: Optional[str] = Field(None, pattern="^[012]$", description="性别")
    birthday: Optional[datetime] = Field(None, description="生日")
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="手机号")
    remark: Optional[str] = Field(None, max_length=200, description="备注")


class FamilyMemberResponse(FamilyMemberBase):
    """家庭成员响应 Schema"""
    uuid: str
    user_id: int
    id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FamilyMemberListResponse(BaseModel):
    """家庭成员列表响应"""
    total: int
    members: list[FamilyMemberResponse]
