"""
数据库连接管理
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from app.core.config import settings

# MySQL 异步引擎（使用 aiomysql 驱动）
# 注意：mysql_url 需要包含 ?async_driver=aiomysql 参数
mysql_url_async = settings.mysql_url.replace("pymysql", "aiomysql")
engine = create_async_engine(
    mysql_url_async,
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
mongo_db = mongo_client["healthpal"]  # 默认数据库

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
    """初始化数据库（仅打印信息，不实际连接）"""
    print("📦 Database status:")
    print(f"   MySQL: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}")
    print(f"   MongoDB: {settings.MONGO_HOST}:{settings.MONGO_PORT}")
    print(f"   Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    print("⚠️  数据库未启动，API 功能受限")
    print("💡 提示：启动 Docker 数据库后重启服务")


async def close_db():
    """关闭数据库连接"""
    print("🔌 Closing database connections...")
    await engine.dispose()
    mongo_client.close()
    await redis_client.close()
