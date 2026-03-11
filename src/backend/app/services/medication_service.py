"""
用药提醒服务
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.medication import MedicationReminder
from typing import List, Tuple, Optional
from datetime import datetime


class MedicationService:
    """用药提醒服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_reminder(
        self,
        user_id: int,
        medication_name: str,
        frequency: str,
        start_date: datetime,
        member_id: Optional[int] = None,
        dosage: Optional[str] = None,
        timing: Optional[list] = None,
        end_date: Optional[datetime] = None,
        instructions: Optional[str] = None,
        notes: Optional[str] = None
    ) -> MedicationReminder:
        """
        创建用药提醒
        
        Args:
            user_id: 用户 ID
            medication_name: 药品名称
            frequency: 用药频率
            start_date: 开始日期
            member_id: 家庭成员 ID（可选）
            dosage: 每次用量（可选）
            timing: 用药时间列表（可选）
            end_date: 结束日期（可选）
            instructions: 用药说明（可选）
            notes: 备注（可选）
            
        Returns:
            创建的 MedicationReminder 对象
        """
        reminder = MedicationReminder(
            user_id=user_id,
            member_id=member_id,
            medication_name=medication_name,
            dosage=dosage,
            frequency=frequency,
            timing=timing,
            start_date=start_date,
            end_date=end_date,
            instructions=instructions,
            notes=notes,
            is_active=True,
            is_completed=False
        )
        
        self.db.add(reminder)
        await self.db.commit()
        await self.db.refresh(reminder)
        
        return reminder
    
    async def get_reminder_by_uuid(self, reminder_uuid: str, user_id: int) -> Optional[dict]:
        """
        根据 UUID 获取用药提醒详情
        
        Args:
            reminder_uuid: 提醒 UUID
            user_id: 用户 ID
            
        Returns:
            提醒详情字典或 None
        """
        result = await self.db.execute(
            select(MedicationReminder).where(
                MedicationReminder.uuid == reminder_uuid,
                MedicationReminder.user_id == user_id,
                MedicationReminder.deleted_at.is_(None)
            )
        )
        
        reminder = result.scalar_one_or_none()
        
        if not reminder:
            return None
        
        return {
            "uuid": reminder.uuid,
            "medication_name": reminder.medication_name,
            "dosage": reminder.dosage,
            "frequency": reminder.frequency,
            "timing": reminder.timing,
            "start_date": reminder.start_date.isoformat(),
            "end_date": reminder.end_date.isoformat() if reminder.end_date else None,
            "is_active": reminder.is_active,
            "is_completed": reminder.is_completed,
            "instructions": reminder.instructions,
            "notes": reminder.notes,
        }
    
    async def get_reminders(
        self,
        user_id: int,
        member_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[dict], int]:
        """
        获取用药提醒列表（分页）
        
        Args:
            user_id: 用户 ID
            member_id: 家庭成员 ID（可选）
            is_active: 是否启用（可选）
            page: 页码
            page_size: 每页大小
            
        Returns:
            (提醒列表，总数)
        """
        # 构建查询
        query = select(MedicationReminder).where(
            MedicationReminder.user_id == user_id,
            MedicationReminder.deleted_at.is_(None)
        )
        
        if member_id is not None:
            query = query.where(MedicationReminder.member_id == member_id)
        
        if is_active is not None:
            query = query.where(MedicationReminder.is_active == is_active)
        
        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        # 分页查询
        query = query.order_by(MedicationReminder.start_date.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        result = await self.db.execute(query)
        reminders = result.scalars().all()
        
        # 转换为字典列表
        reminders_data = [
            {
                "uuid": r.uuid,
                "medication_name": r.medication_name,
                "dosage": r.dosage,
                "frequency": r.frequency,
                "timing": r.timing,
                "start_date": r.start_date.isoformat(),
                "end_date": r.end_date.isoformat() if r.end_date else None,
                "is_active": r.is_active,
                "is_completed": r.is_completed,
                "instructions": r.instructions,
            }
            for r in reminders
        ]
        
        return reminders_data, total
    
    async def update_reminder(
        self,
        reminder_uuid: str,
        user_id: int,
        update_data: dict
    ) -> Optional[MedicationReminder]:
        """
        更新用药提醒
        
        Args:
            reminder_uuid: 提醒 UUID
            user_id: 用户 ID
            update_data: 更新数据字典
            
        Returns:
            更新后的对象或 None
        """
        result = await self.db.execute(
            select(MedicationReminder).where(
                MedicationReminder.uuid == reminder_uuid,
                MedicationReminder.user_id == user_id,
                MedicationReminder.deleted_at.is_(None)
            )
        )
        
        reminder = result.scalar_one_or_none()
        
        if not reminder:
            return None
        
        # 更新字段
        update_fields = [
            "medication_name",
            "dosage",
            "frequency",
            "timing",
            "start_date",
            "end_date",
            "instructions",
            "notes",
            "is_active",
        ]
        
        for field in update_fields:
            if field in update_data and update_data[field] is not None:
                setattr(reminder, field, update_data[field])
        
        await self.db.commit()
        await self.db.refresh(reminder)
        
        return reminder
    
    async def deactivate_reminder(self, reminder_uuid: str, user_id: int) -> bool:
        """
        停用用药提醒
        
        Args:
            reminder_uuid: 提醒 UUID
            user_id: 用户 ID
            
        Returns:
            操作结果：True/False
        """
        result = await self.db.execute(
            select(MedicationReminder).where(
                MedicationReminder.uuid == reminder_uuid,
                MedicationReminder.user_id == user_id
            )
        )
        
        reminder = result.scalar_one_or_none()
        
        if not reminder:
            return False
        
        reminder.is_active = False
        await self.db.commit()
        
        return True
    
    async def confirm_medication(
        self,
        reminder_uuid: str,
        user_id: int,
        taken_time: Optional[datetime] = None,
        notes: Optional[str] = None
    ) -> bool:
        """
        确认用药
        
        Args:
            reminder_uuid: 提醒 UUID
            user_id: 用户 ID
            taken_time: 实际服药时间
            notes: 备注
            
        Returns:
            操作结果：True/False
        """
        # TODO: 实现用药记录功能
        # 目前仅标记为已完成
        result = await self.db.execute(
            select(MedicationReminder).where(
                MedicationReminder.uuid == reminder_uuid,
                MedicationReminder.user_id == user_id
            )
        )
        
        reminder = result.scalar_one_or_none()
        
        if not reminder:
            return False
        
        reminder.is_completed = True
        await self.db.commit()
        
        return True
    
    async def delete_reminder(self, reminder_uuid: str, user_id: int) -> bool:
        """
        软删除用药提醒
        
        Args:
            reminder_uuid: 提醒 UUID
            user_id: 用户 ID
            
        Returns:
            删除结果：True/False
        """
        result = await self.db.execute(
            select(MedicationReminder).where(
                MedicationReminder.uuid == reminder_uuid,
                MedicationReminder.user_id == user_id
            )
        )
        
        reminder = result.scalar_one_or_none()
        
        if not reminder:
            return False
        
        reminder.deleted_at = datetime.utcnow()
        await self.db.commit()
        
        return True
    
    async def get_active_reminders_count(self, user_id: int, member_id: Optional[int] = None) -> int:
        """
        获取活跃的用药提醒数量
        
        Args:
            user_id: 用户 ID
            member_id: 家庭成员 ID（可选）
            
        Returns:
            数量
        """
        query = select(func.count()).where(
            MedicationReminder.user_id == user_id,
            MedicationReminder.is_active == True,
            MedicationReminder.deleted_at.is_(None)
        )
        
        if member_id:
            query = query.where(MedicationReminder.member_id == member_id)
        
        result = await self.db.execute(query)
        return result.scalar()
