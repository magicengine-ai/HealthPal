"""
数据库连接管理
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from app.core.config import settings

# MySQL 异步引擎
engine = create_async_engine(
    settings.mysql_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session 工厂
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# MongoDB 客户端
mongo_client = AsyncIOMotorClient(settings.mongo_url)
mongo_db = mongo_client.get_default_database()

# Redis 客户端
redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


async def get_db() -> AsyncSession:
    """获取数据库 Session（依赖注入）"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_mongo_db():
    """获取 MongoDB 数据库（依赖注入）"""
    return mongo_db


async def get_redis():
    """获取 Redis 客户端（依赖注入）"""
    return redis_client


async def init_db():
    """初始化数据库"""
    print("📦 Initializing databases...")
    
    # 测试 MySQL 连接
    async with engine.connect() as conn:
        print("✅ MySQL connected")
    
    # 测试 MongoDB 连接
    await mongo_client.admin.command('ping')
    print("✅ MongoDB connected")
    
    # 测试 Redis 连接
    await redis_client.ping()
    print("✅ Redis connected")
    
    print("🎉 All databases initialized")


async def close_db():
    """关闭数据库连接"""
    print("🔌 Closing database connections...")
    await engine.dispose()
    mongo_client.close()
    await redis_client.close()
