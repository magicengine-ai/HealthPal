"""
HealthPal Backend - FastAPI 应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    print("🚀 HealthPal Backend Starting...")
    print(f"📡 Environment: {settings.ENV}")
    print(f"📦 Debug Mode: {settings.DEBUG}")
    
    # 初始化数据库连接
    try:
        from app.core.database import init_db
        await init_db()
        print("✅ Database connected")
    except Exception as e:
        print(f"⚠️  数据库未连接：{e}")
        print("💡 提示：启动 Docker 数据库后重启服务")
    
    yield
    
    # 关闭时清理
    print("👋 HealthPal Backend Shutting Down...")
    
    try:
        from app.core.database import close_db
        await close_db()
    except Exception as e:
        print(f"⚠️  关闭数据库连接失败：{e}")


app = FastAPI(
    title="HealthPal API",
    description="个人健康档案 AI 助手 - 后端服务",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查接口"""
    return {"status": "ok", "version": "1.0.0"}


@app.get("/", tags=["根路径"])
async def root():
    """根路径"""
    return {
        "message": "Welcome to HealthPal API",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
