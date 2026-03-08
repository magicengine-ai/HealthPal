"""
用户路由 - 完整版
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from sqlalchemy import select

router = APIRouter()


@router.get("/profile", response_model=UserResponse, summary="获取用户资料")
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户资料"""
    return UserResponse(
        uuid=current_user.uuid,
        phone=current_user.phone,
        nickname=current_user.nickname,
        avatar_url=current_user.avatar_url,
        gender=current_user.gender,
        birthday=current_user.birthday,
        email=current_user.email
    )


@router.put("/profile", response_model=UserResponse, summary="更新用户资料")
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户资料"""
    # 更新字段
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    return UserResponse(
        uuid=current_user.uuid,
        phone=current_user.phone,
        nickname=current_user.nickname,
        avatar_url=current_user.avatar_url,
        gender=current_user.gender,
        birthday=current_user.birthday,
        email=current_user.email
    )


@router.delete("/profile", summary="注销用户")
async def delete_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    注销用户（软删除）
    
    注销后账号将无法登录，但数据会保留
    """
    from datetime import datetime
    current_user.deleted_at = datetime.utcnow()
    await db.commit()
    
    return {"message": "账号已注销"}


@router.get("/family-members", summary="获取家庭成员列表")
async def get_family_members(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户的家庭成员列表"""
    # TODO: 实现家庭成员查询
    return {
        "members": [
            {
                "uuid": "member-001",
                "name": "本人",
                "relation": "本人",
                "is_default": True
            }
        ]
    }


@router.post("/family-members", summary="添加家庭成员")
async def add_family_member(
    member_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加家庭成员"""
    # TODO: 实现家庭成员添加
    return {"message": "TODO: 添加家庭成员"}
