"""
用户服务
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserUpdate
from typing import Optional
from datetime import datetime


class UserService:
    """用户服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_profile(self, user: User) -> dict:
        """
        获取用户资料
        
        Args:
            user: 用户对象
            
        Returns:
            用户资料字典
        """
        return {
            "uuid": user.uuid,
            "user_id": user.id,
            "phone": user.phone,
            "email": user.email,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
            "gender": user.gender,
            "birthday": user.birthday.isoformat() if user.birthday else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
    
    async def update_profile(
        self,
        user: User,
        profile_data: dict
    ) -> User:
        """
        更新用户资料
        
        Args:
            user: 用户对象
            profile_data: 更新数据字典
            
        Returns:
            更新后的 User 对象
        """
        update_fields = [
            "nickname",
            "avatar_url",
            "gender",
            "birthday",
        ]
        
        for field in update_fields:
            if field in profile_data and profile_data[field] is not None:
                setattr(user, field, profile_data[field])
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def update_avatar(self, user: User, avatar_url: str) -> User:
        """
        更新用户头像
        
        Args:
            user: 用户对象
            avatar_url: 头像 URL
            
        Returns:
            更新后的 User 对象
        """
        user.avatar_url = avatar_url
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def delete_account(self, user: User) -> bool:
        """
        删除账户（软删除）
        
        Args:
            user: 用户对象
            
        Returns:
            删除结果：True/False
        """
        user.deleted_at = datetime.utcnow()
        user.phone = f"deleted_{user.phone}"  # 释放手机号
        
        await self.db.commit()
        
        return True
    
    async def check_phone_exists(self, phone: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        检查手机号是否已存在
        
        Args:
            phone: 手机号
            exclude_user_id: 排除的用户 ID（用于更新时）
            
        Returns:
            是否存在：True/False
        """
        query = select(User).where(
            User.phone == phone,
            User.deleted_at.is_(None)
        )
        
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)
        
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        return user is not None
    
    async def check_email_exists(self, email: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        检查邮箱是否已存在
        
        Args:
            email: 邮箱
            exclude_user_id: 排除的用户 ID（用于更新时）
            
        Returns:
            是否存在：True/False
        """
        query = select(User).where(
            User.email == email,
            User.deleted_at.is_(None)
        )
        
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)
        
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        return user is not None
    
    async def bind_email(self, user: User, email: str) -> bool:
        """
        绑定邮箱
        
        Args:
            user: 用户对象
            email: 邮箱地址
            
        Returns:
            绑定结果：True/False
        """
        # 检查邮箱是否已被其他用户使用
        exists = await self.check_email_exists(email, exclude_user_id=user.id)
        if exists:
            return False
        
        user.email = email
        await self.db.commit()
        
        return True
    
    async def get_user_statistics(self, user: User) -> dict:
        """
        获取用户统计信息
        
        Args:
            user: 用户对象
            
        Returns:
            统计信息字典
        """
        from app.models.family_member import FamilyMember
        from app.models.health_record import HealthRecord
        from app.models.medication import MedicationReminder
        
        # 家庭成员数量
        family_count = await self.db.execute(
            select(FamilyMember).where(
                FamilyMember.user_id == user.id,
                FamilyMember.deleted_at.is_(None)
            )
        )
        family_total = len(family_count.scalars().all())
        
        # 健康档案数量
        record_count = await self.db.execute(
            select(HealthRecord).where(
                HealthRecord.user_id == user.id,
                HealthRecord.deleted_at.is_(None)
            )
        )
        record_total = len(record_count.scalars().all())
        
        # 用药提醒数量
        medication_count = await self.db.execute(
            select(MedicationReminder).where(
                MedicationReminder.user_id == user.id,
                MedicationReminder.deleted_at.is_(None),
                MedicationReminder.is_active == True
            )
        )
        medication_total = len(medication_count.scalars().all())
        
        return {
            "family_members": family_total,
            "health_records": record_total,
            "active_medications": medication_total,
        }
