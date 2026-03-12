"""
OCR 相关异步任务
"""
import asyncio
import httpx
from datetime import datetime, timedelta
from celery import Task
from app.core.celery_config import celery_app
from app.core.config import settings
from app.services.ocr_service import OCRService
from app.services.record_service import RecordService
from app.db.mysql import get_db
from app.db.mongodb import get_mongodb


@celery_app.task(bind=True, max_retries=3)
def process_ocr_task(self, record_id: str, file_path: str, ocr_provider: str = "baidu"):
    """
    异步处理 OCR 识别任务
    
    Args:
        record_id: 档案记录 ID
        file_path: 文件路径
        ocr_provider: OCR 服务提供商 (baidu/tencent)
    """
    try:
        db = next(get_db())
        db_client = asyncio.run(get_mongodb())
        
        ocr_service = OCRService(db, db_client)
        record_service = RecordService(db, db_client)
        
        # 更新状态为处理中
        record_service.update_ocr_status(record_id, status=1, message="OCR 识别中...")
        
        # 调用 OCR 服务
        ocr_result = asyncio.run(ocr_service.process_document(file_path, ocr_provider))
        
        if ocr_result.get('success'):
            # 提取指标数据
            indicators = asyncio.run(ocr_service.extract_indicators(ocr_result.get('text', '')))
            
            # 更新档案记录
            record_service.update_ocr_status(
                record_id,
                status=2,
                message="OCR 识别完成",
                ocr_text=ocr_result.get('text', ''),
                indicators=indicators
            )
            
            return {
                'success': True,
                'record_id': record_id,
                'indicators_count': len(indicators),
                'message': 'OCR 识别完成'
            }
        else:
            # OCR 失败
            record_service.update_ocr_status(
                record_id,
                status=3,
                message=f"OCR 识别失败：{ocr_result.get('error', '未知错误')}"
            )
            
            return {
                'success': False,
                'record_id': record_id,
                'error': ocr_result.get('error')
            }
            
    except Exception as e:
        # 重试逻辑
        try:
            raise self.retry(exc=e, countdown=60)  # 60 秒后重试
        except self.MaxRetriesExceededError:
            # 超过最大重试次数，标记为失败
            record_service.update_ocr_status(
                record_id,
                status=3,
                message=f"OCR 识别失败（重试{self.max_retries}次后仍失败）: {str(e)}"
            )
            return {
                'success': False,
                'record_id': record_id,
                'error': str(e)
            }


@celery_app.task(bind=True)
def poll_ocr_status(self, record_id: str, max_attempts: int = 30):
    """
    轮询 OCR 处理状态（用于第三方异步 OCR API）
    
    Args:
        record_id: 档案记录 ID
        max_attempts: 最大轮询次数
    """
    try:
        db = next(get_db())
        db_client = asyncio.run(get_mongodb())
        
        record_service = RecordService(db, db_client)
        record = record_service.get_record_by_id(record_id)
        
        if not record:
            return {'success': False, 'error': '记录不存在'}
        
        # 检查 OCR 状态
        ocr_status = record.get('ocr_status', 0)
        
        if ocr_status == 2:  # 已完成
            return {
                'success': True,
                'record_id': record_id,
                'status': 'completed'
            }
        elif ocr_status == 3:  # 失败
            return {
                'success': False,
                'record_id': record_id,
                'status': 'failed'
            }
        
        # 继续轮询
        if self.request.retries < max_attempts:
            raise self.retry(countdown=2)  # 每 2 秒轮询一次
        
        # 超时
        record_service.update_ocr_status(
            record_id,
            status=3,
            message="OCR 识别超时"
        )
        
        return {
            'success': False,
            'record_id': record_id,
            'status': 'timeout'
        }
        
    except Exception as e:
        raise self.retry(exc=e, countdown=2)


@celery_app.task
def cleanup_expired_files(days: int = 30):
    """
    清理过期的临时文件
    
    Args:
        days: 保留天数，默认 30 天
    """
    import os
    import shutil
    
    try:
        upload_dir = settings.UPLOAD_DIR
        cutoff_date = datetime.now() - timedelta(days=days)
        cleaned_count = 0
        
        for root, dirs, files in os.walk(upload_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if file_mtime < cutoff_date:
                    os.remove(file_path)
                    cleaned_count += 1
            
            # 清理空目录
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    shutil.rmtree(dir_path)
        
        return {
            'success': True,
            'cleaned_files': cleaned_count,
            'message': f'清理了 {cleaned_count} 个过期文件'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@celery_app.task
def batch_process_ocr(record_ids: list):
    """
    批量处理 OCR 任务
    
    Args:
        record_ids: 档案记录 ID 列表
    """
    results = []
    
    for record_id in record_ids:
        # 异步调用单个 OCR 任务
        result = process_ocr_task.delay(record_id, "pending")
        results.append({
            'record_id': record_id,
            'task_id': result.id
        })
    
    return {
        'success': True,
        'total': len(record_ids),
        'tasks': results
    }
