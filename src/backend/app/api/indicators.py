"""
健康指标 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.indicator import (
    IndicatorCreate,
    IndicatorResponse,
    IndicatorTrendResponse,
    IndicatorListResponse,
)
from app.schemas.common import ResponseModel
from app.services.indicator_service import IndicatorService
from app.services.record_service import RecordService

router = APIRouter(prefix="/indicators", tags=["健康指标"])


@router.post("", response_model=ResponseModel, summary="手动添加指标")
async def create_indicator(
    indicator_data: IndicatorCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """手动添加健康指标"""
    indicator_service = IndicatorService(db)
    
    try:
        indicator = await indicator_service.create_indicator(
            record_uuid=indicator_data.record_uuid,
            user_id=current_user.id,
            indicator_code=indicator_data.indicator_code,
            indicator_name=indicator_data.indicator_name,
            value=indicator_data.value,
            test_date=indicator_data.test_date.isoformat(),
            unit=indicator_data.unit,
            reference_min=indicator_data.reference_min,
            reference_max=indicator_data.reference_max,
            member_id=indicator_data.member_id
        )
        
        return ResponseModel(
            code=0,
            message="添加成功",
            data={
                "uuid": indicator.uuid,
                "id": indicator.id
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/trend", response_model=ResponseModel, summary="获取指标趋势")
async def get_indicator_trend(
    indicator_code: str = Query(..., description="指标代码"),
    member_id: Optional[int] = None,
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取指标趋势数据"""
    indicator_service = IndicatorService(db)
    
    trend_data = await indicator_service.get_indicator_trend(
        user_id=current_user.id,
        indicator_code=indicator_code,
        member_id=member_id,
        limit=limit
    )
    
    return ResponseModel(
        code=0,
        data={
            "indicator_code": indicator_code,
            "data_points": trend_data
        }
    )


@router.get("/statistics", response_model=ResponseModel, summary="获取指标统计")
async def get_indicator_statistics(
    indicator_code: str = Query(..., description="指标代码"),
    member_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取指标统计信息（平均值、最小值、最大值）"""
    indicator_service = IndicatorService(db)
    
    stats = await indicator_service.get_statistics(
        user_id=current_user.id,
        indicator_code=indicator_code,
        member_id=member_id
    )
    
    return ResponseModel(
        code=0,
        data=stats
    )


@router.get("/record/{record_id}", response_model=ResponseModel, summary="获取档案指标列表")
async def get_indicators_by_record(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取指定档案的所有指标"""
    record_service = RecordService(db)
    
    record = await record_service.get_record_by_uuid(record_id, current_user.id)
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="档案不存在"
        )
    
    return ResponseModel(
        code=0,
        data={
            "record_uuid": record_id,
            "indicators": record.get("indicators", [])
        }
    )


@router.delete("/{indicator_id}", response_model=ResponseModel, summary="删除指标")
async def delete_indicator(
    indicator_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除健康指标"""
    indicator_service = IndicatorService(db)
    
    success = await indicator_service.delete_indicator(indicator_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指标不存在"
        )
    
    return ResponseModel(
        code=0,
        message="删除成功"
    )
