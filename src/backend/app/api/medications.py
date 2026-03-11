"""
用药提醒 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.medication import (
    MedicationCreate,
    MedicationUpdate,
    MedicationResponse,
    MedicationListResponse,
    MedicationConfirmRequest,
)
from app.schemas.common import ResponseModel
from app.services.medication_service import MedicationService

router = APIRouter(prefix="/medications", tags=["用药提醒"])


@router.post("/reminders", response_model=ResponseModel, summary="创建用药提醒")
async def create_medication_reminder(
    reminder_data: MedicationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建用药提醒"""
    medication_service = MedicationService(db)
    
    reminder = await medication_service.create_reminder(
        user_id=current_user.id,
        member_id=reminder_data.member_id,
        medication_name=reminder_data.medication_name,
        dosage=reminder_data.dosage,
        frequency=reminder_data.frequency,
        timing=[t.model_dump() for t in reminder_data.timing] if reminder_data.timing else None,
        start_date=reminder_data.start_date,
        end_date=reminder_data.end_date,
        instructions=reminder_data.instructions,
        notes=reminder_data.notes
    )
    
    return ResponseModel(
        code=0,
        message="创建成功",
        data={
            "uuid": reminder.uuid,
            "id": reminder.id
        }
    )


@router.get("/reminders", response_model=ResponseModel, summary="获取用药提醒列表")
async def get_medication_reminders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    member_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用药提醒列表（分页）"""
    medication_service = MedicationService(db)
    
    reminders, total = await medication_service.get_reminders(
        user_id=current_user.id,
        member_id=member_id,
        is_active=is_active,
        page=page,
        page_size=page_size
    )
    
    return ResponseModel(
        code=0,
        data={
            "total": total,
            "page": page,
            "page_size": page_size,
            "medications": reminders
        }
    )


@router.get("/reminders/{reminder_id}", response_model=ResponseModel, summary="获取用药提醒详情")
async def get_medication_reminder(
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用药提醒详情"""
    medication_service = MedicationService(db)
    
    reminder = await medication_service.get_reminder_by_uuid(reminder_id, current_user.id)
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用药提醒不存在"
        )
    
    return ResponseModel(
        code=0,
        data=reminder
    )


@router.put("/reminders/{reminder_id}", response_model=ResponseModel, summary="更新用药提醒")
async def update_medication_reminder(
    reminder_id: str,
    reminder_data: MedicationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用药提醒"""
    medication_service = MedicationService(db)
    
    update_data = reminder_data.model_dump(exclude_unset=True)
    
    reminder = await medication_service.update_reminder(
        reminder_uuid=reminder_id,
        user_id=current_user.id,
        update_data=update_data
    )
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用药提醒不存在"
        )
    
    return ResponseModel(
        code=0,
        message="更新成功"
    )


@router.post("/reminders/{reminder_id}/confirm", response_model=ResponseModel, summary="确认用药")
async def confirm_medication(
    reminder_id: str,
    confirm_data: Optional[MedicationConfirmRequest] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """确认已用药"""
    medication_service = MedicationService(db)
    
    taken_time = confirm_data.taken_time if confirm_data else None
    notes = confirm_data.notes if confirm_data else None
    
    success = await medication_service.confirm_medication(
        reminder_uuid=reminder_id,
        user_id=current_user.id,
        taken_time=taken_time,
        notes=notes
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用药提醒不存在"
        )
    
    return ResponseModel(
        code=0,
        message="确认成功"
    )


@router.post("/reminders/{reminder_id}/deactivate", response_model=ResponseModel, summary="停用用药提醒")
async def deactivate_medication_reminder(
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """停用用药提醒"""
    medication_service = MedicationService(db)
    
    success = await medication_service.deactivate_reminder(reminder_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用药提醒不存在"
        )
    
    return ResponseModel(
        code=0,
        message="停用成功"
    )


@router.delete("/reminders/{reminder_id}", response_model=ResponseModel, summary="删除用药提醒")
async def delete_medication_reminder(
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """软删除用药提醒"""
    medication_service = MedicationService(db)
    
    success = await medication_service.delete_reminder(reminder_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用药提醒不存在"
        )
    
    return ResponseModel(
        code=0,
        message="删除成功"
    )
