"""
健康档案服务
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.health_record import HealthRecord
from app.models.health_indicator import HealthIndicator
from app.services.file_service import FileService
from app.services.ocr_service import OCRService
from typing import List, Tuple, Optional
from datetime import datetime
import uuid


class RecordService:
    """健康档案服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.file_service = FileService()
        self.ocr_service = OCRService()
    
    async def create_record(
        self,
        user_id: int,
        record_type: str,
        title: str,
        record_date: str,
        member_id: Optional[int] = None,
        hospital: Optional[str] = None,
        department: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> HealthRecord:
        """
        创建健康档案记录
        
        Args:
            user_id: 用户 ID
            record_type: 档案类型
            title: 档案标题
            record_date: 检查日期 (YYYY-MM-DD)
            member_id: 家庭成员 ID（可选）
            hospital: 医院名称（可选）
            department: 科室（可选）
            tags: 标签列表（可选）
            
        Returns:
            创建的 HealthRecord 对象
        """
        record = HealthRecord(
            user_id=user_id,
            member_id=member_id,
            record_type=record_type,
            title=title,
            hospital=hospital,
            department=department,
            record_date=datetime.strptime(record_date, "%Y-%m-%d").date(),
            tags=tags or [],
            ocr_status="pending"
        )
        
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        
        return record
    
    async def get_record_by_uuid(self, record_uuid: str, user_id: int) -> Optional[dict]:
        """
        根据 UUID 获取档案详情
        
        Args:
            record_uuid: 档案 UUID
            user_id: 用户 ID
            
        Returns:
            档案详情字典或 None
        """
        result = await self.db.execute(
            select(HealthRecord).where(
                HealthRecord.uuid == record_uuid,
                HealthRecord.user_id == user_id,
                HealthRecord.deleted_at.is_(None)
            )
        )
        
        record = result.scalar_one_or_none()
        
        if not record:
            return None
        
        # 获取关联的指标
        indicators_result = await self.db.execute(
            select(HealthIndicator).where(
                HealthIndicator.record_id == record.id
            )
        )
        indicators = indicators_result.scalars().all()
        
        return {
            "uuid": record.uuid,
            "title": record.title,
            "record_type": record.record_type,
            "hospital": record.hospital,
            "department": record.department,
            "record_date": record.record_date.isoformat(),
            "ocr_status": record.ocr_status,
            "ocr_result": record.ocr_result,
            "structured_data": record.structured_data,
            "tags": record.tags or [],
            "file_urls": record.file_urls or [],
            "indicators": [
                {
                    "uuid": i.uuid,
                    "code": i.indicator_code,
                    "name": i.indicator_name,
                    "value": i.value,
                    "unit": i.unit,
                    "reference_min": i.reference_min,
                    "reference_max": i.reference_max,
                    "status": i.status
                }
                for i in indicators
            ]
        }
    
    async def get_records(
        self,
        user_id: int,
        member_id: Optional[int] = None,
        record_type: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[dict], int]:
        """
        获取档案列表（分页）
        
        Args:
            user_id: 用户 ID
            member_id: 家庭成员 ID（可选）
            record_type: 档案类型（可选）
            page: 页码
            page_size: 每页大小
            
        Returns:
            (档案列表，总数)
        """
        # 构建查询
        query = select(HealthRecord).where(
            HealthRecord.user_id == user_id,
            HealthRecord.deleted_at.is_(None)
        )
        
        if member_id:
            query = query.where(HealthRecord.member_id == member_id)
        
        if record_type:
            query = query.where(HealthRecord.record_type == record_type)
        
        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        # 分页查询
        query = query.order_by(HealthRecord.record_date.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        result = await self.db.execute(query)
        records = result.scalars().all()
        
        # 转换为字典列表
        records_data = [
            {
                "uuid": r.uuid,
                "title": r.title,
                "record_type": r.record_type,
                "hospital": r.hospital,
                "department": r.department,
                "record_date": r.record_date.isoformat(),
                "ocr_status": r.ocr_status,
                "file_urls": r.file_urls or [],
                "tags": r.tags or [],
            }
            for r in records
        ]
        
        return records_data, total
    
    async def update_record_files(self, record_uuid: str, file_urls: List[str]) -> bool:
        """
        更新档案文件 URL
        
        Args:
            record_uuid: 档案 UUID
            file_urls: 文件 URL 列表
            
        Returns:
            更新结果：True/False
        """
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.uuid == record_uuid)
        )
        record = result.scalar_one_or_none()
        
        if not record:
            return False
        
        record.file_urls = file_urls
        await self.db.commit()
        
        return True
    
    async def update_ocr_status(
        self,
        record_uuid: str,
        status: str,
        ocr_result: Optional[dict] = None,
        structured_data: Optional[dict] = None
    ) -> bool:
        """
        更新 OCR 状态
        
        Args:
            record_uuid: 档案 UUID
            status: OCR 状态
            ocr_result: OCR 原始结果
            structured_data: 结构化数据
            
        Returns:
            更新结果：True/False
        """
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.uuid == record_uuid)
        )
        record = result.scalar_one_or_none()
        
        if not record:
            return False
        
        record.ocr_status = status
        
        if ocr_result:
            record.ocr_result = ocr_result
        
        if structured_data:
            record.structured_data = structured_data
        
        await self.db.commit()
        
        return True
    
    async def trigger_ocr_task(self, record_uuid: str, file_url: str) -> bool:
        """
        触发 OCR 识别任务
        
        Args:
            record_uuid: 档案 UUID
            file_url: 文件 URL
            
        Returns:
            触发结果：True/False
        """
        # 先更新状态为处理中
        success = await self.update_ocr_status(record_uuid, "processing")
        
        if not success:
            return False
        
        # TODO: 触发异步任务（Celery）
        # 暂时同步执行
        await self._process_ocr_sync(record_uuid, file_url)
        
        return True
    
    async def _process_ocr_sync(self, record_uuid: str, file_url: str):
        """
        同步处理 OCR（临时方案）
        
        Args:
            record_uuid: 档案 UUID
            file_url: 文件 URL
        """
        try:
            # 调用 OCR 识别
            ocr_result = self.ocr_service.recognize(file_url)
            
            if not ocr_result:
                await self.update_ocr_status(record_uuid, "failed")
                return
            
            # 解析结果
            structured_data = self.ocr_service.parse_ocr_result(ocr_result)
            
            # 更新状态
            await self.update_ocr_status(
                record_uuid,
                "completed",
                ocr_result,
                structured_data
            )
            
            # 提取指标并保存
            if structured_data.get("indicators"):
                await self._save_indicators_from_ocr(
                    record_uuid,
                    structured_data["indicators"]
                )
            
        except Exception as e:
            print(f"OCR 处理失败：{e}")
            await self.update_ocr_status(record_uuid, "failed")
    
    async def _save_indicators_from_ocr(
        self,
        record_uuid: str,
        indicators: List[dict]
    ):
        """
        从 OCR 结果保存指标
        
        Args:
            record_uuid: 档案 UUID
            indicators: 指标列表
        """
        record_result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.uuid == record_uuid)
        )
        record = record_result.scalar_one_or_none()
        
        if not record:
            return
        
        for ind_data in indicators:
            indicator = HealthIndicator(
                record_id=record.id,
                user_id=record.user_id,
                member_id=record.member_id,
                indicator_code=ind_data.get("indicator_name", ""),
                indicator_name=ind_data.get("indicator_name", ""),
                value=ind_data.get("value", ""),
                unit=ind_data.get("unit", ""),
                test_date=record.record_date
            )
            self.db.add(indicator)
        
        await self.db.commit()
    
    async def delete_record(self, record_uuid: str, user_id: int) -> bool:
        """
        软删除档案
        
        Args:
            record_uuid: 档案 UUID
            user_id: 用户 ID
            
        Returns:
            删除结果：True/False
        """
        result = await self.db.execute(
            select(HealthRecord).where(
                HealthRecord.uuid == record_uuid,
                HealthRecord.user_id == user_id
            )
        )
        record = result.scalar_one_or_none()
        
        if not record:
            return False
        
        record.deleted_at = datetime.utcnow()
        await self.db.commit()
        
        return True
