"""
依赖注入
"""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.utils.jwt import verify_token
from app.models.user import User
from typing import Optional

# OAuth2 方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    
    Args:
        token: JWT Token
        db: 数据库会话
        
    Returns:
        User 对象
        
    Raises:
        HTTPException: 认证失败
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="认证失败",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    # 验证 Token
    token_data = verify_token(token)
    if not token_data or not token_data.uuid:
        raise credentials_exception
    
    # 查询用户
    from sqlalchemy import select
    result = await db.execute(
        select(User).where(
            User.uuid == token_data.uuid,
            User.deleted_at.is_(None)
        )
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise credentials_exception
    
    return user


async def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    获取当前用户（可选，允许未登录）
    
    Args:
        token: JWT Token
        db: 数据库会话
        
    Returns:
        User 对象或 None
    """
    try:
        return await get_current_user(token, db)
    except HTTPException:
        return None


def get_db_session() -> AsyncSession:
    """获取数据库会话（用于非路由场景）"""
    from app.core.database import async_session_maker
    return async_session_maker()
