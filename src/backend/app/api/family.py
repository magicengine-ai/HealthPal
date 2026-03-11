"""
家庭成员 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.family_member import FamilyMember
from app.schemas.family import (
    FamilyMemberCreate,
    FamilyMemberUpdate,
    FamilyMemberResponse,
    FamilyMemberListResponse,
)
from app.schemas.common import ResponseModel
from app.services.user_service import UserService
from sqlalchemy import select
from datetime import datetime

router = APIRouter(prefix="/family", tags=["家庭成员"])


@router.get("/members", response_model=ResponseModel, summary="获取家庭成员列表")
async def get_family_members(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取家庭成员列表"""
    query = select(FamilyMember).where(
        FamilyMember.user_id == current_user.id,
        FamilyMember.deleted_at.is_(None)
    ).order_by(FamilyMember.created_at.desc())
    
    # 分页
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    result = await db.execute(query)
    members = result.scalars().all()
    
    # 获取总数
    count_query = select(FamilyMember).where(
        FamilyMember.user_id == current_user.id,
        FamilyMember.deleted_at.is_(None)
    )
    total_result = await db.execute(count_query)
    total = len(total_result.scalars().all())
    
    return ResponseModel(
        code=0,
        data={
            "total": total,
            "page": page,
            "page_size": page_size,
            "members": [
                {
                    "uuid": m.uuid,
                    "name": m.name,
                    "relation": m.relation,
                    "gender": m.gender,
                    "birthday": m.birthday.isoformat() if m.birthday else None,
                    "phone": m.phone,
                    "remark": m.remark,
                }
                for m in members
            ]
        }
    )


@router.post("/members", response_model=ResponseModel, summary="添加家庭成员")
async def create_family_member(
    member_data: FamilyMemberCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加家庭成员"""
    member = FamilyMember(
        user_id=current_user.id,
        name=member_data.name,
        relation=member_data.relation,
        gender=member_data.gender,
        birthday=member_data.birthday,
        phone=member_data.phone,
        remark=member_data.remark
    )
    
    db.add(member)
    await db.commit()
    await db.refresh(member)
    
    return ResponseModel(
        code=0,
        message="添加成功",
        data={
            "uuid": member.uuid,
            "id": member.id
        }
    )


@router.get("/members/{member_id}", response_model=ResponseModel, summary="获取家庭成员详情")
async def get_family_member(
    member_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取家庭成员详情"""
    result = await db.execute(
        select(FamilyMember).where(
            FamilyMember.id == member_id,
            FamilyMember.user_id == current_user.id,
            FamilyMember.deleted_at.is_(None)
        )
    )
    
    member = result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家庭成员不存在"
        )
    
    return ResponseModel(
        code=0,
        data={
            "uuid": member.uuid,
            "name": member.name,
            "relation": member.relation,
            "gender": member.gender,
            "birthday": member.birthday.isoformat() if member.birthday else None,
            "phone": member.phone,
            "remark": member.remark,
        }
    )


@router.put("/members/{member_id}", response_model=ResponseModel, summary="更新家庭成员")
async def update_family_member(
    member_id: int,
    member_data: FamilyMemberUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新家庭成员信息"""
    result = await db.execute(
        select(FamilyMember).where(
            FamilyMember.id == member_id,
            FamilyMember.user_id == current_user.id,
            FamilyMember.deleted_at.is_(None)
        )
    )
    
    member = result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家庭成员不存在"
        )
    
    # 更新字段
    update_data = member_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(member, field, value)
    
    await db.commit()
    await db.refresh(member)
    
    return ResponseModel(
        code=0,
        message="更新成功"
    )


@router.delete("/members/{member_id}", response_model=ResponseModel, summary="删除家庭成员")
async def delete_family_member(
    member_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """软删除家庭成员"""
    result = await db.execute(
        select(FamilyMember).where(
            FamilyMember.id == member_id,
            FamilyMember.user_id == current_user.id,
            FamilyMember.deleted_at.is_(None)
        )
    )
    
    member = result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家庭成员不存在"
        )
    
    member.deleted_at = datetime.utcnow()
    await db.commit()
    
    return ResponseModel(
        code=0,
        message="删除成功"
    )
