"""
API 路由汇总
"""
from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.family import router as family_router
from app.api.records import router as records_router
from app.api.indicators import router as indicators_router
from app.api.medications import router as medications_router

# 创建主路由
api_router = APIRouter()

# 包含所有子路由
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(family_router)
api_router.include_router(records_router)
api_router.include_router(indicators_router)
api_router.include_router(medications_router)
