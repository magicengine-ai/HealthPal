"""
认证路由 - 完整版
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import uuid

from app.core.database import get_db, redis_client
from app.core.security import verify_password, get_password_hash, create_access_token, decode_token
from app.core.config import settings
from app.core.auth import get_current_user, blacklist_token, check_token_blacklist, security
from app.models.user import User
from app.schemas.user import (
    UserCreate, UserLogin, TokenResponse, UserResponse,
    PasswordReset, PasswordChange, UserUpdate
)
from app.services.sms import get_sms_service
from sqlalchemy import select

router = APIRouter()


@router.post("/register", response_model=TokenResponse, summary="用户注册")
async def register(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册
    
    - **phone**: 手机号（11 位中国大陆手机号）
    - **password**: 密码（6-32 位）
    - **verify_code**: 短信验证码
    - **nickname**: 昵称（可选）
    """
    # 验证短信验证码
    sms_service = get_sms_service(redis_client)
    is_valid = await sms_service.verify_code(user_data.phone, user_data.verify_code)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误或已过期"
        )
    
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
    - **verify_code**: 验证码（可选，首次登录或异地登录需要）
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
    
    # 检查用户是否被删除
    if user.deleted_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户已被删除"
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


@router.post("/logout", summary="用户登出")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    用户登出
    
    将当前 Token 加入黑名单
    """
    token = credentials.credentials
    
    # 解码 Token 获取过期时间
    payload = decode_token(token)
    if payload:
        exp = payload.get("exp", 0)
        expire_seconds = max(0, exp - int(datetime.utcnow().timestamp()))
        
        # 加入黑名单
        await blacklist_token(token, expire_seconds)
    
    return {"message": "登出成功"}


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前登录用户信息"""
    return UserResponse(
        uuid=current_user.uuid,
        phone=current_user.phone,
        nickname=current_user.nickname,
        avatar_url=current_user.avatar_url,
        gender=current_user.gender,
        birthday=current_user.birthday,
        email=current_user.email
    )


@router.put("/me", response_model=UserResponse, summary="更新用户信息")
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新当前用户信息"""
    # 更新字段
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    return UserResponse(
        uuid=current_user.uuid,
        phone=current_user.phone,
        nickname=current_user.nickname,
        avatar_url=current_user.avatar_url,
        gender=current_user.gender,
        birthday=current_user.birthday,
        email=current_user.email
    )


@router.post("/send-code", summary="发送短信验证码")
async def send_verification_code(
    phone: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    发送短信验证码
    
    - **phone**: 手机号
    """
    # 验证手机号格式
    import re
    if not re.match(r'^1[3-9]\d{9}$', phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号格式错误"
        )
    
    # 检查手机号是否已注册（根据场景可选）
    # result = await db.execute(select(User).where(User.phone == phone))
    # if result.scalar_one_or_none():
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="手机号已注册"
    #     )
    
    # 发送验证码
    sms_service = get_sms_service(redis_client)
    success = await sms_service.send_code(phone)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="发送过于频繁，请稍后再试"
        )
    
    return {"message": "验证码已发送", "expire_in": 300}


@router.post("/reset-password", summary="重置密码")
async def reset_password(
    password_data: PasswordReset,
    db: AsyncSession = Depends(get_db)
):
    """
    重置密码
    
    - **phone**: 手机号
    - **verify_code**: 短信验证码
    - **new_password**: 新密码
    """
    # 验证短信验证码
    sms_service = get_sms_service(redis_client)
    is_valid = await sms_service.verify_code(password_data.phone, password_data.verify_code)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误或已过期"
        )
    
    # 查询用户
    result = await db.execute(
        select(User).where(User.phone == password_data.phone)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 更新密码
    user.password_hash = get_password_hash(password_data.new_password)
    await db.commit()
    
    return {"message": "密码重置成功"}


@router.post("/change-password", summary="修改密码")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    修改密码（需要登录）
    
    - **old_password**: 旧密码
    - **new_password**: 新密码
    """
    # 验证旧密码
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误"
        )
    
    # 更新密码
    current_user.password_hash = get_password_hash(password_data.new_password)
    await db.commit()
    
    return {"message": "密码修改成功"}
