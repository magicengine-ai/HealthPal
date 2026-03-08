"""
应用配置管理
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """应用配置"""
    
    # 基础配置
    ENV: str = "development"
    DEBUG: bool = True
    APP_NAME: str = "HealthPal"
    API_PREFIX: str = "/api/v1"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "healthpal"
    MYSQL_PASSWORD: str = "healthpal_pass"
    MYSQL_DATABASE: str = "healthpal"
    
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_USER: str = "healthpal"
    MONGO_PASSWORD: str = "healthpal_pass"
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # JWT 配置
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 天
    
    # CORS 配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
    ]
    
    # 文件存储配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # OCR 服务配置
    OCR_API_KEY: str = ""
    OCR_API_SECRET: str = ""
    OCR_PROVIDER: str = "baidu"  # baidu/tencent
    
    # 推送服务配置
    PUSH_PROVIDER: str = "jiguang"  # jiguang/getui
    
    @property
    def mysql_url(self) -> str:
        """MySQL 连接 URL"""
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
    
    @property
    def mongo_url(self) -> str:
        """MongoDB 连接 URL"""
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/"
    
    @property
    def redis_url(self) -> str:
        """Redis 连接 URL"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()
