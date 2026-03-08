"""
短信验证码服务
"""
import random
import string
from typing import Optional
from datetime import datetime, timedelta
import redis.asyncio as redis
from app.core.config import settings


class SMSCodeService:
    """短信验证码服务"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.code_length = 6
        self.expire_minutes = 5
        self.max_attempts = 3
    
    def generate_code(self) -> str:
        """生成随机验证码"""
        return ''.join(random.choices(string.digits, k=self.code_length))
    
    async def send_code(self, phone: str) -> bool:
        """
        发送短信验证码
        
        实际项目中需要集成短信服务商（阿里云/腾讯云）
        这里仅做演示，打印验证码到日志
        """
        # 检查发送频率限制
        rate_limit_key = f"sms:rate_limit:{phone}"
        if await self.redis.exists(rate_limit_key):
            return False
        
        # 生成验证码
        code = self.generate_code()
        
        # 存储验证码（5 分钟有效期）
        code_key = f"sms:code:{phone}"
        await self.redis.setex(
            code_key,
            timedelta(minutes=self.expire_minutes),
            code
        )
        
        # 设置发送频率限制（60 秒内只能发送一次）
        await self.redis.setex(
            rate_limit_key,
            timedelta(seconds=60),
            "1"
        )
        
        # 重置验证尝试次数
        attempt_key = f"sms:attempts:{phone}"
        await self.redis.set(attempt_key, "0")
        
        # TODO: 调用短信服务商 API
        # 这里仅打印到日志
        print(f"📱 短信验证码 [{phone}]: {code}")
        
        return True
    
    async def verify_code(self, phone: str, code: str) -> bool:
        """验证短信验证码"""
        code_key = f"sms:code:{phone}"
        stored_code = await self.redis.get(code_key)
        
        if not stored_code:
            return False
        
        if stored_code != code:
            # 增加失败尝试次数
            attempt_key = f"sms:attempts:{phone}"
            attempts = int(await self.redis.get(attempt_key) or "0") + 1
            
            if attempts >= self.max_attempts:
                # 超过最大尝试次数，删除验证码
                await self.redis.delete(code_key)
            else:
                await self.redis.set(attempt_key, str(attempts))
            
            return False
        
        # 验证成功，删除验证码
        await self.redis.delete(code_key)
        await self.redis.delete(f"sms:attempts:{phone}")
        
        return True


# 全局服务实例（依赖注入时创建）
sms_service: Optional[SMSCodeService] = None


def get_sms_service(redis_client: redis.Redis) -> SMSCodeService:
    """获取短信服务实例"""
    global sms_service
    if sms_service is None:
        sms_service = SMSCodeService(redis_client)
    return sms_service
