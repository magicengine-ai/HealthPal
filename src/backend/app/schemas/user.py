"""
用户数据模式（Pydantic Schemas）
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime


class UserBase(BaseModel):
    """用户基础模式"""
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像 URL")
    gender: Optional[int] = Field(0, ge=0, le=2, description="性别 0:未知 1:男 2:女")
    birthday: Optional[date] = Field(None, description="生日")


class UserCreate(BaseModel):
    """用户创建模式"""
    phone: str = Field(..., pattern=r'^1[3-9]\d{9}$', description="手机号")
    password: str = Field(..., min_length=6, max_length=32, description="密码")
    verify_code: str = Field(..., min_length=6, max_length=6, description="验证码")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")


class UserLogin(BaseModel):
    """用户登录模式"""
    phone: str = Field(..., pattern=r'^1[3-9]\d{9}$', description="手机号")
    password: str = Field(..., description="密码")
    verify_code: Optional[str] = Field(None, min_length=6, max_length=6, description="验证码")


class UserResponse(UserBase):
    """用户响应模式"""
    uuid: str
    phone: str
    email: Optional[str] = None
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token 响应模式"""
    token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
