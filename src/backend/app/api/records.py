"""
健康档案 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.record import (
    RecordCreate,
    RecordResponse,
    RecordListResponse,
    RecordUploadResponse,
)
from app.schemas.common import ResponseModel
from app.services.record_service import RecordService
from app.services.file_service import FileService
from app.utils.validator import validate_date_format

router = APIRouter(prefix="/records", tags=["健康档案"])


@router.post("/upload", response_model=ResponseModel, summary="上传健康档案")
async def upload_record(
    file: UploadFile = File(..., description="图片/PDF 文件"),
    record_type: str = Form(..., description="档案类型"),
    title: str = Form(..., description="档案标题"),
    record_date: str = Form(..., description="检查日期"),
    member_id: Optional[int] = Form(None, description="家庭成员 ID"),
    hospital: Optional[str] = Form(None, description="医院名称"),
    department: Optional[str] = Form(None, description="科室"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    上传健康档案
    
    支持格式：JPG, PNG, PDF
    最大大小：10MB
    """
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的文件格式，支持 JPG/PNG/PDF"
        )
    
    # 验证日期格式
    if not validate_date_format(record_date):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="日期格式错误，应为 YYYY-MM-DD"
        )
    
    # 读取文件内容
    content = await file.read()
    
    # 验证文件大小（10MB）
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小超过 10MB"
        )
    
    record_service = RecordService(db)
    file_service = FileService()
    
    # 创建档案记录
    record = await record_service.create_record(
        user_id=current_user.id,
        member_id=member_id,
        record_type=record_type,
        title=title,
        record_date=record_date,
        hospital=hospital,
        department=department
    )
    
    # 上传文件
    file_url = await file_service.upload_file(
        content=content,
        filename=file.filename,
        content_type=file.content_type,
        record_uuid=record.uuid
    )
    
    # 更新档案文件 URL
    await record_service.update_record_files(record.uuid, [file_url])
    
    # 触发 OCR 识别
    await record_service.trigger_ocr_task(record.uuid, file_url)
    
    return ResponseModel(
        code=0,
        message="上传成功",
        data={
            "record_id": record.uuid,
            "ocr_status": "pending"
        }
    )


@router.get("", response_model=ResponseModel, summary="获取档案列表")
async def get_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    member_id: Optional[int] = None,
    record_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取健康档案列表（分页）"""
    record_service = RecordService(db)
    
    records, total = await record_service.get_records(
        user_id=current_user.id,
        member_id=member_id,
        record_type=record_type,
        page=page,
        page_size=page_size
    )
    
    return ResponseModel(
        code=0,
        data={
            "total": total,
            "page": page,
            "page_size": page_size,
            "records": records
        }
    )


@router.get("/{record_id}", response_model=ResponseModel, summary="获取档案详情")
async def get_record_detail(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取健康档案详情"""
    record_service = RecordService(db)
    
    record = await record_service.get_record_by_uuid(record_id, current_user.id)
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="档案不存在"
        )
    
    return ResponseModel(
        code=0,
        data=record
    )


@router.delete("/{record_id}", response_model=ResponseModel, summary="删除档案")
async def delete_record(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除健康档案（软删除）"""
    record_service = RecordService(db)
    
    success = await record_service.delete_record(record_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="档案不存在"
        )
    
    return ResponseModel(
        code=0,
        message="删除成功"
    )


@router.get("/{record_id}/indicators", response_model=ResponseModel, summary="获取档案指标")
async def get_record_indicators(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取档案中的健康指标"""
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
            "indicators": record.get("indicators", [])
        }
    )
