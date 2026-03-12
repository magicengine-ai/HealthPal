"""
异步任务 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from celery.result import AsyncResult
from app.core.celery_config import celery_app
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import ResponseModel

router = APIRouter(prefix="/tasks", tags=["异步任务"])


@router.get("/{task_id}", response_model=ResponseModel, summary="查询任务状态")
async def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    查询异步任务执行状态
    
    任务状态：
    - PENDING: 等待执行
    - STARTED: 正在执行
    - SUCCESS: 执行成功
    - FAILURE: 执行失败
    - RETRY: 重试中
    """
    result = AsyncResult(task_id, app=celery_app)
    
    response_data = {
        "task_id": task_id,
        "status": result.status,
        "ready": result.ready()
    }
    
    if result.ready():
        response_data["result"] = result.result
        if result.failed() and result.result:
            response_data["error"] = str(result.result)
    
    return ResponseModel(
        code=0,
        data=response_data
    )


@router.post("/revoke/{task_id}", response_model=ResponseModel, summary="撤销任务")
async def revoke_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    撤销正在执行的异步任务
    
    注意：只能撤销尚未开始执行的任务
    """
    from celery.exceptions import TimeoutError
    
    try:
        result = AsyncResult(task_id, app=celery_app)
        
        if result.ready():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="任务已完成，无法撤销"
            )
        
        # 撤销任务
        celery_app.control.revoke(task_id, terminate=True)
        
        return ResponseModel(
            code=0,
            message="任务已撤销",
            data={
                "task_id": task_id,
                "status": "revoked"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"撤销失败：{str(e)}"
        )


@router.get("/ocr/{record_id}", response_model=ResponseModel, summary="查询 OCR 任务状态")
async def get_ocr_task_status(
    record_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    查询指定档案的 OCR 识别任务状态
    
    返回最新的 OCR 任务状态
    """
    # TODO: 从数据库查询档案的 OCR 任务 ID
    # 这里简化处理，直接返回档案状态
    
    from app.db.mongodb import get_mongodb
    import asyncio
    
    db_client = asyncio.run(get_mongodb())
    record = db_client['healthpal']['records'].find_one({"uuid": record_id})
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="档案不存在"
        )
    
    return ResponseModel(
        code=0,
        data={
            "record_id": record_id,
            "ocr_status": record.get("ocr_status", 0),
            "ocr_message": record.get("ocr_message", "未知"),
            "indicators_count": len(record.get("indicators", []))
        }
    )
