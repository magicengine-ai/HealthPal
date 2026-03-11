"""
Redis 客户端配置
"""
import redis.asyncio as redis
from app.core.config import settings

# Redis 客户端
redis_client = redis.Redis.from_url(
    settings.redis_url,
    decode_responses=True
)


async def get_redis() -> redis.Redis:
    """获取 Redis 客户端（依赖注入）"""
    return redis_client


async def close_redis():
    """关闭 Redis 连接"""
    await redis_client.close()
