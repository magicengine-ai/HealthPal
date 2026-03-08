"""
健康档案路由
"""
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db

router = APIRouter()


@router.post("/upload", summary="上传健康文档")
async def upload_record(
    file: UploadFile = File(..., description="健康文档图片/PDF"),
    member_id: Optional[str] = Form(None, description="家庭成员 ID"),
    record_type: str = Form(..., description="文档类型：体检报告/病历/处方/检查单"),
    title: str = Form(..., description="文档标题"),
    record_date: str = Form(..., description="文档日期 YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db)
):
    """
    上传健康文档
    
    - **file**: 图片/PDF 文件
    - **record_type**: 文档类型
    - **title**: 文档标题
    - **record_date**: 文档日期
    - **member_id**: 家庭成员 ID（可选，默认为本人）
    """
    # TODO: 文件保存
    # TODO: 调用 OCR 服务
    # TODO: 数据库记录
    
    return {
        "message": "TODO: 上传健康文档",
        "file": file.filename,
        "record_type": record_type
    }


@router.get("/", summary="获取档案列表")
async def get_records(
    page: int = 1,
    page_size: int = 20,
    member_id: Optional[str] = None,
    record_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """获取健康档案列表"""
    return {"message": "TODO: 获取档案列表"}


@router.get("/{record_id}", summary="获取档案详情")
async def get_record(record_id: str, db: AsyncSession = Depends(get_db)):
    """获取健康档案详情"""
    return {"message": "TODO: 获取档案详情"}


@router.delete("/{record_id}", summary="删除档案")
async def delete_record(record_id: str, db: AsyncSession = Depends(get_db)):
    """删除健康档案"""
    return {"message": "TODO: 删除档案"}
