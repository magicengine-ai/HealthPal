"""
用药管理路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db

router = APIRouter()


@router.post("/reminders", summary="创建用药提醒")
async def create_reminder(
    medicine_name: str,
    dosage: str,
    frequency: str,
    reminder_times: list,
    start_date: str,
    end_date: Optional[str] = None,
    member_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """创建用药提醒"""
    return {"message": "TODO: 创建用药提醒"}


@router.get("/reminders", summary="获取提醒列表")
async def get_reminders(
    status: Optional[int] = 1,
    db: AsyncSession = Depends(get_db)
):
    """获取用药提醒列表"""
    return {"message": "TODO: 获取提醒列表"}


@router.post("/reminders/{reminder_id}/confirm", summary="确认用药")
async def confirm_medication(
    reminder_id: int,
    take_time: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """确认已用药"""
    return {"message": "TODO: 确认用药"}
