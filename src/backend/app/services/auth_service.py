"""
认证服务
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token, verify_token
from app.db.redis import redis_client
from app.utils.validator import validate_verify_code
from typing import Optional
import uuid


class AuthService:
    """认证服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_phone(self, phone: str) -> Optional[User]:
        """
        根据手机号获取用户
        
        Args:
            phone: 手机号
            
        Returns:
            User 对象或 None
        """
        result = await self.db.execute(
            select(User).where(
                User.phone == phone,
                User.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_uuid(self, uuid: str) -> Optional[User]:
        """
        根据 UUID 获取用户
        
        Args:
            uuid: 用户 UUID
            
        Returns:
            User 对象或 None
        """
        result = await self.db.execute(
            select(User).where(
                User.uuid == uuid,
                User.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        根据 ID 获取用户
        
        Args:
            user_id: 用户 ID
            
        Returns:
            User 对象或 None
        """
        result = await self.db.execute(
            select(User).where(
                User.id == user_id,
                User.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()
    
    async def create_user(
        self,
        phone: str,
        password: str,
        nickname: Optional[str] = None,
        email: Optional[str] = None
    ) -> User:
        """
        创建新用户
        
        Args:
            phone: 手机号
            password: 密码（明文）
            nickname: 昵称（可选）
            email: 邮箱（可选）
            
        Returns:
            创建的 User 对象
        """
        password_hash = hash_password(password)
        
        user = User(
            phone=phone,
            password_hash=password_hash,
            nickname=nickname,
            email=email
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def authenticate_user(self, phone: str, password: str) -> Optional[User]:
        """
        验证用户登录
        
        Args:
            phone: 手机号
            password: 密码（明文）
            
        Returns:
            User 对象或 None（验证失败）
        """
        user = await self.get_user_by_phone(phone)
        
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        return user
    
    async def create_access_token(self, user_uuid: str) -> str:
        """
        生成访问 Token
        
        Args:
            user_uuid: 用户 UUID
            
        Returns:
            JWT Token 字符串
        """
        return create_access_token(data={"sub": user_uuid})
    
    async def verify_sms_code(self, phone: str, code: str) -> bool:
        """
        验证短信验证码
        
        Args:
            phone: 手机号
            code: 验证码
            
        Returns:
            验证结果：True/False
        """
        key = f"sms:code:{phone}"
        stored_code = await redis_client.get(key)
        
        if not stored_code:
            return False
        
        return stored_code == code
    
    async def set_sms_code(self, phone: str, code: str, expire: int = 300):
        """
        设置短信验证码（5 分钟有效期）
        
        Args:
            phone: 手机号
            code: 验证码
            expire: 有效期（秒），默认 300 秒
        """
        key = f"sms:code:{phone}"
        await redis_client.setex(key, expire, code)
    
    async def send_sms_code(self, phone: str) -> bool:
        """
        发送短信验证码
        
        Args:
            phone: 手机号
            
        Returns:
            发送结果：True/False
        """
        from app.services.sms import SmsService
        
        # 生成 6 位验证码
        import random
        code = str(random.randint(100000, 999999))
        
        # 发送短信
        sms_service = SmsService()
        success = await sms_service.send_verify_code(phone, code)
        
        if success:
            # 存储验证码到 Redis
            await self.set_sms_code(phone, code)
        
        return success
    
    async def change_password(
        self,
        user: User,
        old_password: str,
        new_password: str
    ) -> bool:
        """
        修改密码
        
        Args:
            user: 用户对象
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            修改结果：True/False
        """
        # 验证旧密码
        if not verify_password(old_password, user.password_hash):
            return False
        
        # 更新密码
        user.password_hash = hash_password(new_password)
        await self.db.commit()
        
        return True
    
    async def blacklist_token(self, token: str, expire: int = 3600):
        """
        将 Token 加入黑名单
        
        Args:
            token: JWT Token
            expire: 过期时间（秒）
        """
        from app.utils.jwt import decode_token
        
        payload = decode_token(token)
        if payload:
            jti = payload.get("jti", str(uuid.uuid4()))
            key = f"token:blacklist:{jti}"
            await redis_client.setex(key, expire, "1")
    
    async def is_token_blacklisted(self, token: str) -> bool:
        """
        检查 Token 是否在黑名单中
        
        Args:
            token: JWT Token
            
        Returns:
            检查结果：True/False
        """
        from app.utils.jwt import decode_token
        
        payload = decode_token(token)
        if payload:
            jti = payload.get("jti", str(uuid.uuid4()))
            key = f"token:blacklist:{jti}"
            exists = await redis_client.exists(key)
            return bool(exists)
        
        return False
