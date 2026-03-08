"""
HealthPal Backend - FastAPI 应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import auth, users, records, indicators, medications


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    print("🚀 HealthPal Backend Starting...")
    print(f"📡 Environment: {settings.ENV}")
    print(f"📦 Debug Mode: {settings.DEBUG}")
    
    # 初始化数据库连接等
    # await init_db()
    
    yield
    
    # 关闭时清理
    print("👋 HealthPal Backend Shutting Down...")
    # await close_db()


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

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/v1/users", tags=["用户"])
app.include_router(records.router, prefix="/api/v1/records", tags=["健康档案"])
app.include_router(indicators.router, prefix="/api/v1/indicators", tags=["健康指标"])
app.include_router(medications.router, prefix="/api/v1/medications", tags=["用药管理"])


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
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
