"""
用户数据模式（Pydantic Schemas）- 完整版
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re


class UserBase(BaseModel):
    """用户基础模式"""
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像 URL")
    gender: Optional[int] = Field(0, ge=0, le=2, description="性别 0:未知 1:男 2:女")
    birthday: Optional[date] = Field(None, description="生日")


class UserCreate(BaseModel):
    """用户注册模式"""
    phone: str = Field(..., description="手机号")
    password: str = Field(..., min_length=6, max_length=32, description="密码")
    verify_code: str = Field(..., min_length=6, max_length=6, description="验证码")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号格式错误')
        return v


class UserLogin(BaseModel):
    """用户登录模式"""
    phone: str = Field(..., description="手机号")
    password: str = Field(..., description="密码")
    verify_code: Optional[str] = Field(None, min_length=6, max_length=6, description="验证码")
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号格式错误')
        return v


class UserResponse(UserBase):
    """用户响应模式"""
    uuid: str
    phone: str
    email: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """用户更新模式"""
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像 URL")
    gender: Optional[int] = Field(None, ge=0, le=2, description="性别")
    birthday: Optional[date] = Field(None, description="生日")
    email: Optional[EmailStr] = Field(None, description="邮箱")


class TokenResponse(BaseModel):
    """Token 响应模式"""
    token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class PasswordReset(BaseModel):
    """密码重置模式"""
    phone: str = Field(..., description="手机号")
    verify_code: str = Field(..., min_length=6, max_length=6, description="验证码")
    new_password: str = Field(..., min_length=6, max_length=32, description="新密码")
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号格式错误')
        return v


class PasswordChange(BaseModel):
    """密码修改模式（已登录）"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, max_length=32, description="新密码")


class SMSCodeRequest(BaseModel):
    """短信验证码请求模式"""
    phone: str = Field(..., description="手机号")
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号格式错误')
        return v
