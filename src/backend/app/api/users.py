"""
用户路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter()


@router.get("/profile", summary="获取用户资料")
async def get_profile(db: AsyncSession = Depends(get_db)):
    """获取当前用户资料"""
    return {"message": "TODO: 获取用户资料"}


@router.put("/profile", summary="更新用户资料")
async def update_profile(db: AsyncSession = Depends(get_db)):
    """更新用户资料"""
    return {"message": "TODO: 更新用户资料"}
