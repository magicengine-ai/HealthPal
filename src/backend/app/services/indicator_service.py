"""
健康指标服务
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.health_indicator import HealthIndicator
from app.models.health_record import HealthRecord
from typing import List, Tuple, Optional
from datetime import datetime, date


class IndicatorService:
    """健康指标服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_indicator(
        self,
        record_uuid: str,
        user_id: int,
        indicator_code: str,
        indicator_name: str,
        value: str,
        test_date: str,
        unit: Optional[str] = None,
        reference_min: Optional[str] = None,
        reference_max: Optional[str] = None,
        member_id: Optional[int] = None
    ) -> HealthIndicator:
        """
        创建健康指标
        
        Args:
            record_uuid: 档案 UUID
            user_id: 用户 ID
            indicator_code: 指标代码
            indicator_name: 指标名称
            value: 检测值
            test_date: 检测日期
            unit: 单位（可选）
            reference_min: 参考范围最小值（可选）
            reference_max: 参考范围最大值（可选）
            member_id: 家庭成员 ID（可选）
            
        Returns:
            创建的 HealthIndicator 对象
        """
        # 获取档案
        record_result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.uuid == record_uuid)
        )
        record = record_result.scalar_one_or_none()
        
        if not record:
            raise ValueError(f"档案不存在：{record_uuid}")
        
        # 创建指标
        indicator = HealthIndicator(
            record_id=record.id,
            user_id=user_id,
            member_id=member_id or record.member_id,
            indicator_code=indicator_code,
            indicator_name=indicator_name,
            value=value,
            unit=unit,
            reference_min=reference_min,
            reference_max=reference_max,
            test_date=datetime.strptime(test_date, "%Y-%m-%d").date()
        )
        
        # 自动判断状态
        indicator.status = self._calculate_status(value, reference_min, reference_max)
        
        self.db.add(indicator)
        await self.db.commit()
        await self.db.refresh(indicator)
        
        return indicator
    
    def _calculate_status(
        self,
        value: str,
        ref_min: Optional[str],
        ref_max: Optional[str]
    ) -> str:
        """
        计算指标状态（正常/偏低/偏高）
        
        Args:
            value: 检测值
            ref_min: 参考范围最小值
            ref_max: 参考范围最大值
            
        Returns:
            状态字符串
        """
        if not ref_min or not ref_max:
            return "unknown"
        
        try:
            val = float(value)
            min_val = float(ref_min)
            max_val = float(ref_max)
            
            if val < min_val:
                return "low"
            elif val > max_val:
                return "high"
            else:
                return "normal"
        except (ValueError, TypeError):
            return "unknown"
    
    async def get_indicators_by_record(
        self,
        record_uuid: str,
        user_id: int
    ) -> List[dict]:
        """
        获取档案的指标列表
        
        Args:
            record_uuid: 档案 UUID
            user_id: 用户 ID
            
        Returns:
            指标列表
        """
        # 先获取档案
        record_result = await self.db.execute(
            select(HealthRecord).where(
                HealthRecord.uuid == record_uuid,
                HealthRecord.user_id == user_id
            )
        )
        record = record_result.scalar_one_or_none()
        
        if not record:
            return []
        
        # 获取指标
        result = await self.db.execute(
            select(HealthIndicator).where(
                HealthIndicator.record_id == record.id
            ).order_by(HealthIndicator.indicator_name)
        )
        
        indicators = result.scalars().all()
        
        return [
            {
                "uuid": i.uuid,
                "code": i.indicator_code,
                "name": i.indicator_name,
                "value": i.value,
                "unit": i.unit,
                "reference_min": i.reference_min,
                "reference_max": i.reference_max,
                "status": i.status,
            }
            for i in indicators
        ]
    
    async def get_indicator_trend(
        self,
        user_id: int,
        indicator_code: str,
        member_id: Optional[int] = None,
        limit: int = 10
    ) -> List[dict]:
        """
        获取指标趋势数据
        
        Args:
            user_id: 用户 ID
            indicator_code: 指标代码
            member_id: 家庭成员 ID（可选）
            limit: 返回数量限制
            
        Returns:
            趋势数据列表
        """
        query = select(HealthIndicator).where(
            HealthIndicator.user_id == user_id,
            HealthIndicator.indicator_code == indicator_code
        )
        
        if member_id:
            query = query.where(HealthIndicator.member_id == member_id)
        
        query = query.order_by(HealthIndicator.test_date.desc()).limit(limit)
        
        result = await self.db.execute(query)
        indicators = result.scalars().all()
        
        # 按日期正序排列
        indicators = sorted(indicators, key=lambda x: x.test_date)
        
        return [
            {
                "date": i.test_date.isoformat(),
                "value": i.value,
                "unit": i.unit,
                "status": i.status,
            }
            for i in indicators
        ]
    
    async def get_statistics(
        self,
        user_id: int,
        indicator_code: str,
        member_id: Optional[int] = None
    ) -> dict:
        """
        获取指标统计信息
        
        Args:
            user_id: 用户 ID
            indicator_code: 指标代码
            member_id: 家庭成员 ID（可选）
            
        Returns:
            统计信息字典
        """
        query = select(
            func.avg(HealthIndicator.value.cast(float)),
            func.min(HealthIndicator.value.cast(float)),
            func.max(HealthIndicator.value.cast(float)),
            func.count(HealthIndicator.id)
        ).where(
            HealthIndicator.user_id == user_id,
            HealthIndicator.indicator_code == indicator_code
        )
        
        if member_id:
            query = query.where(HealthIndicator.member_id == member_id)
        
        result = await self.db.execute(query)
        row = result.first()
        
        if not row or row[3] == 0:
            return {
                "avg": None,
                "min": None,
                "max": None,
                "count": 0,
            }
        
        return {
            "avg": round(row[0], 2) if row[0] else None,
            "min": row[1],
            "max": row[2],
            "count": row[3],
        }
    
    async def delete_indicator(self, indicator_uuid: str, user_id: int) -> bool:
        """
        删除指标
        
        Args:
            indicator_uuid: 指标 UUID
            user_id: 用户 ID
            
        Returns:
            删除结果：True/False
        """
        result = await self.db.execute(
            select(HealthIndicator).where(
                HealthIndicator.uuid == indicator_uuid,
                HealthIndicator.user_id == user_id
            )
        )
        indicator = result.scalar_one_or_none()
        
        if not indicator:
            return False
        
        await self.db.delete(indicator)
        await self.db.commit()
        
        return True
