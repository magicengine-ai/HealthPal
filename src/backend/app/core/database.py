"""
数据库连接管理
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from app.core.config import settings


# ==================== Base Class ====================

class Base(AsyncAttrs, DeclarativeBase):
    """SQLAlchemy 基础模型类"""
    pass


# ==================== MySQL ====================

# MySQL 异步引擎（使用 aiomysql 驱动）- WSL2 使用 socket 连接
mysql_socket = "/var/run/mysqld/mysqld.sock"
mysql_url_async = f"mysql+aiomysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@localhost/{settings.MYSQL_DATABASE}?unix_socket={mysql_socket}&charset=utf8mb4"

engine = create_async_engine(
    mysql_url_async,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,  # 1 小时回收连接
)

# Session 工厂
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# ==================== MongoDB ====================

mongo_url = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}/"
mongo_client = AsyncIOMotorClient(mongo_url)
mongo_db = mongo_client["healthpal"]  # 默认数据库


# ==================== Redis ====================

redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
redis_client = redis.Redis.from_url(redis_url, decode_responses=True)


# ==================== Dependency Injection ====================

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


# ==================== Database Initialization ====================

async def create_tables():
    """创建所有数据库表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully")


async def drop_tables():
    """删除所有数据库表（慎用！）"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("⚠️  All database tables dropped")


async def init_db():
    """初始化数据库连接"""
    print("📦 Database connections:")
    print(f"   MySQL: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}")
    print(f"   MongoDB: {settings.MONGO_HOST}:{settings.MONGO_PORT}")
    print(f"   Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    
    # 测试连接（可选）
    if settings.DEBUG:
        try:
            async with engine.connect() as conn:
                print("✅ MySQL connection successful")
        except Exception as e:
            print(f"⚠️  MySQL connection failed: {e}")
    
    try:
        await redis_client.ping()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"⚠️  Redis connection failed: {e}")


async def close_db():
    """关闭数据库连接"""
    print("🔌 Closing database connections...")
    await engine.dispose()
    mongo_client.close()
    await redis_client.close()
    print("✅ All connections closed")
