"""
健康指标路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db

router = APIRouter()


@router.get("/trend", summary="获取指标趋势")
async def get_indicator_trend(
    indicator_code: str,
    member_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    获取指标趋势数据
    
    - **indicator_code**: 指标编码（BP_HIGH/BS/GLU 等）
    - **member_id**: 家庭成员 ID
    - **start_date**: 开始日期
    - **end_date**: 结束日期
    """
    return {
        "message": "TODO: 获取指标趋势",
        "indicator_code": indicator_code
    }


@router.post("/", summary="手动添加指标")
async def add_indicator(
    indicator_code: str,
    value: float,
    unit: str,
    measure_date: str,
    member_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """手动添加健康指标"""
    return {"message": "TODO: 添加指标"}
