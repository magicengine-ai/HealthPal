"""
认证路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
import uuid

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from sqlalchemy import select

router = APIRouter()


@router.post("/register", response_model=TokenResponse, summary="用户注册")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    用户注册
    
    - **phone**: 手机号
    - **password**: 密码（6-32 位）
    - **verify_code**: 短信验证码
    - **nickname**: 昵称（可选）
    """
    # TODO: 验证短信验证码
    
    # 检查手机号是否已存在
    result = await db.execute(
        select(User).where(User.phone == user_data.phone)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号已注册"
        )
    
    # 创建新用户
    new_user = User(
        uuid=str(uuid.uuid4()),
        phone=user_data.phone,
        password_hash=get_password_hash(user_data.password),
        nickname=user_data.nickname or f"用户{user_data.phone[-4:]}"
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # 生成 Token
    access_token = create_access_token(
        data={"sub": new_user.uuid, "type": "access"}
    )
    
    return TokenResponse(
        token=access_token,
        token_type="bearer",
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            uuid=new_user.uuid,
            phone=new_user.phone,
            nickname=new_user.nickname,
            avatar_url=new_user.avatar_url,
            gender=new_user.gender,
            birthday=new_user.birthday
        )
    )


@router.post("/login", response_model=TokenResponse, summary="用户登录")
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    用户登录
    
    - **phone**: 手机号
    - **password**: 密码
    - **verify_code**: 验证码（可选，首次登录需要）
    """
    # 查询用户
    result = await db.execute(
        select(User).where(User.phone == credentials.phone)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成 Token
    access_token = create_access_token(
        data={"sub": user.uuid, "type": "access"}
    )
    
    return TokenResponse(
        token=access_token,
        token_type="bearer",
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            uuid=user.uuid,
            phone=user.phone,
            nickname=user.nickname,
            avatar_url=user.avatar_url,
            gender=user.gender,
            birthday=user.birthday
        )
    )


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user(
    # TODO: 添加认证依赖
    db: AsyncSession = Depends(get_db)
):
    """获取当前登录用户信息"""
    # TODO: 从 Token 中解析用户 UUID
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="认证功能开发中"
    )
